from textual.app import App

from unctl.interactive.screens.quit_confirm import QuitConfirm
from unctl.interactive.screens.problem import ProblemScreen


class DebugApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("q", "request_quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()

    def on_mount(self):
        self.push_screen(ProblemScreen())

    def action_request_quit(self):
        self.push_screen(QuitConfirm())
