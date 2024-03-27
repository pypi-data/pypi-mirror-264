from rich.console import Console
from rich.style import Style
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.highlighter import RegexHighlighter

from textual import events
from textual.app import App, ComposeResult
from textual.widgets import RichLog


class CmdLog(RichLog):

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield RichLog(highlight=True, markup=True)

    def call_update(self, slog: str):
        text_log = self.query_one(RichLog)
        text_log.write(slog)
