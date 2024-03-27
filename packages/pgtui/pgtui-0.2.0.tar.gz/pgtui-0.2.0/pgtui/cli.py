import logging

from textual.logging import TextualHandler
from pgtui.app import PgTuiApp


def main():
    logging.basicConfig(level="NOTSET", handlers=[TextualHandler()])
    PgTuiApp().run()
