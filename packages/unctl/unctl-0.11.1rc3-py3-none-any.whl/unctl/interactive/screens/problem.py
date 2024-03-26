from typing import cast
from textual import on, work

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Footer, Header, TextArea, Select
from textual.containers import Container
from unctl.interactive.screens.resolving import ResolvingScreen
from unctl.lib.llm.assistant import OpenAIAssistant
from unctl.lib.llm.utils import set_llm_instance
from unctl.lib.reports.report import Report
from unctl.constants import CheckProviders


class ProblemScreen(Screen):
    TITLE = "Describe the problem"
    BINDINGS = [
        ("s", "start_resolving", "Start resolving"),
    ]
    CSS_PATH = "preview.tcss"

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        textarea = TextArea(
            id="problem-body",
        )
        textarea.show_line_numbers = False
        yield Container(
            Static("Select provider:", id="provider-title"),
            Select(
                options=(
                    (line, line)
                    for line in [
                        CheckProviders.AWS,
                        CheckProviders.K8S,
                        CheckProviders.MySQL,
                    ]
                ),
                allow_blank=False,
            ),
            Static("Tell us about your problem:", id="problem-title"),
            textarea,
            id="container",
        )

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value.value)

    def lock_operations(self):
        placeholder = self.query_one(Container)
        placeholder.loading = True

    def unlock_operations(self):
        placeholder = self.query_one(Container)
        placeholder.loading = False

    def show_error_message(self, error_message: str):
        # Show an error. Set a longer timeout so it's noticed.
        self.notify(error_message, severity="error", timeout=2)

    def action_start_resolving(self):
        provider = self.query_one(Select)

        if provider.value is None:
            self.show_error_message("Please select a provider")
            return

        selected_provider = cast(str, provider.value)

        # Check if the selected provider is among the supported providers
        if selected_provider not in CheckProviders.__members__.values():
            return

        # create LLM instance based on provider
        llm_helper = OpenAIAssistant(provider.value)
        # FIXME: prevent llm_instance to set to None
        set_llm_instance(llm_helper)
        self.lock_operations()
        self.initialise_recommendations()

    @work
    async def initialise_recommendations(self):
        problem = self.query_one(TextArea)
        item = Report(problem.text)

        await item.init_llm_session()
        await item.get_next_steps()

        self.app.push_screen(ResolvingScreen(item))
        self.unlock_operations()
