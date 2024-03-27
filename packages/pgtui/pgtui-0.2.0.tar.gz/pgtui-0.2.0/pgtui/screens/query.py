import logging
from asyncio import Lock
from datetime import datetime

from psycopg import Column, Error
from psycopg.rows import TupleRow
from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Header, TextArea

from pgtui.db import execute
from pgtui.entities import DbInfo, ResultMeta
from pgtui.messages import RunQuery, ShowException
from pgtui.utils.datetime import format_duration
from pgtui.widgets.editor import SqlEditor
from pgtui.widgets.footer import DbFooter
from pgtui.widgets.results import ResultsTable
from pgtui.widgets.status_bar import StatusBar

logger = logging.getLogger(__name__)


class QueryScreen(Screen[None]):
    CSS = """
    SqlEditor {
        height: 50%;
    }

    ResultsTable {
        height: 50%;
        border: solid black;
        &:focus {
            border: tall $accent;
        }
    }
    """

    def __init__(self, db_info: DbInfo):
        super().__init__()
        self.execLock = Lock()
        self.db_info = db_info

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(SqlEditor(), ResultsTable())
        yield StatusBar()
        yield DbFooter(self.db_info)

    def on_mount(self):
        self.query_one(TextArea).focus()

    async def on_run_query(self, message: RunQuery):
        self.run_query(message.query)

    @work
    async def run_query(self, query: str):
        self.show_status("Running query...")

        if self.execLock.locked():
            return

        try:
            async with self.execLock:
                meta = await self._execute(query)
                self.show_status_meta(meta)
        except Error as ex:
            logger.info(f"Query failed: {ex}")
            self.show_status("")
            self.post_message(ShowException(ex))

    async def _execute(self, query: str) -> ResultMeta:
        start = datetime.now()
        async with execute(query) as cursor:
            if cursor.rowcount > 0:
                rows = await cursor.fetchall()
                duration = datetime.now() - start
                self.display_data(rows, cursor.description)
            else:
                duration = datetime.now() - start
            return ResultMeta(cursor.rowcount, duration)

    def display_data(self, rows: list[TupleRow], columns: list[Column] | None):
        column_names = (c.name for c in columns) if columns else None
        with self.app.batch_update():
            self.query(ResultsTable).remove()
            table = ResultsTable(rows, column_names)
            self.mount(table, after=self.query_one(SqlEditor))

    def show_status(self, message: str):
        self.query_one(StatusBar).set_message(message)

    def show_status_meta(self, meta: ResultMeta):
        duration = format_duration(meta.duration)
        message = f"Done. {meta.rows} rows. {duration}"
        self.query_one(StatusBar).set_message(message)
