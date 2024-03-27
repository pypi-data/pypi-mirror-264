import logging
from asyncio import Lock

from textual.app import App

from pgtui.db import fetch_db_info
from pgtui.messages import ShowException
from pgtui.screens.loading import LoadingScreen
from pgtui.screens.query import QueryScreen
from pgtui.widgets.dialog import MessageDialog

logger = logging.getLogger(__name__)


class PgTuiApp(App[None]):
    def __init__(self):
        super().__init__()
        self.execLock = Lock()

    def on_mount(self):
        self.push_screen(LoadingScreen())
        self.call_after_refresh(self.db_init)

    async def db_init(self):
        db_info = await fetch_db_info()
        await self.switch_screen(QueryScreen(db_info))

    def on_show_exception(self, message: ShowException):
        body = str(message.exception)
        self.push_screen(MessageDialog("Error", body, error=True))
