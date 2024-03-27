from itertools import cycle
from typing import Any, Iterable

from psycopg.rows import TupleRow
from textual.widgets import DataTable
from textual.widgets.data_table import CursorType


class ResultsTable(DataTable[Any]):
    BINDINGS = [
        ("s", "toggle_cursor", "Selection"),
    ]

    def __init__(
        self,
        rows: Iterable[TupleRow] | None = None,
        columns: Iterable[str] | None = None,
    ):
        super().__init__()
        self.cursors: Iterable[CursorType] = cycle(["cell", "row", "column", "none"])
        self.cursor_type = next(self.cursors)

        if columns:
            self.add_columns(*columns)

        if rows:
            self.add_rows(rows)

    def action_toggle_cursor(self):
        self.cursor_type = next(self.cursors)
