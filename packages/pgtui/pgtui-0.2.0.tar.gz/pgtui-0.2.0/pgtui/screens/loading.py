from rich import markup
from textual.screen import Screen
from textual.widgets import Label

from pgtui import __version__


class LoadingScreen(Screen[None]):
    DEFAULT_CSS = """
    LoadingScreen {
        align: center middle;
        background: $panel;
    }

    LoadingScreen > Label {
        width: 100%;
        color: white;
        text-align: center;
    }
    """

    def compose(self):
        yield Label(f"[b]pgtui {markup.escape(__version__)}[/b]")
        yield Label("Connecting…")
