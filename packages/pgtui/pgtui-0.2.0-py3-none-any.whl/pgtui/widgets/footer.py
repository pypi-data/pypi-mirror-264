from itertools import chain

from rich.text import Text
from textual.widget import Widget

from pgtui.db import DbInfo


class DbFooter(Widget):
    COMPONENT_CLASSES = {"dbfooter--highlight"}

    DEFAULT_CSS = """
    DbFooter {
        background: $accent;
        color: $text;
        dock: bottom;
        height: 1;
    }
    DbFooter > .dbfooter--highlight {
        background: $accent-darken-1;
    }
    """

    def __init__(self, db_info: DbInfo):
        super().__init__()
        self.db_info = db_info

    def render(self):
        highlight_style = self.get_component_rich_style("dbfooter--highlight")

        info = {
            "Database": self.db_info.database,
            "Schema": self.db_info.schema,
            "User": self.db_info.user,
            "Host": self.db_info.host,
            "Port": self.db_info.port,
            "Address": self.db_info.host_address,
        }

        parts = chain.from_iterable(
            [f" {name} ", (f" {value} ", highlight_style)] for name, value in info.items() if value
        )

        return Text.assemble(*parts)
