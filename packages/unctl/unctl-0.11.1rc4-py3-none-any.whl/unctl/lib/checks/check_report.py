import abc
from typing import Literal
from unctl.lib.utils import exec_cmd
from dataclasses import dataclass, field
from re import findall

from unctl.lib.models.checks import CheckMetadataModel
from unctl.lib.reports.report import Report


@dataclass
class CheckReport(Report):
    """Contains the Check's finding information."""

    check_metadata: CheckMetadataModel = field(init=False)

    status: Literal["PASS", "FAIL"] | None = None
    status_extended: str = ""

    def _fill_tmpl_cmd(self, cmd: str | list[str]) -> tuple[str]:
        # TODO: switch to proper template tool
        result = []
        if not isinstance(cmd, list):
            cmd = [cmd]
        for part in cmd:
            for p in _find_substrings(part):
                if getattr(self, p) is None or len(getattr(self, p)) == 0:
                    print(f"Error: {p} is None for {self.object_id}")
                    break
                part = part.replace("{{" + p + "}}", getattr(self, p))

            if len(_find_substrings(part)) != 0:
                print(f"Error: {part} has unresolved parameters for {self.unique_name}")
                return None
            result.append(part)

        return tuple(result)

    async def init_llm_session(self):
        """Initializes AI LLM component"""
        data = [
            (
                f"Help me resolve problem ```{self.status_extended}```"
                f"for object ```{self.unique_name}```."
            )
        ]
        data.extend(self.cmd_output_messages)
        await self._session_keeper.init_session(data=data)

    async def execute_diagnostics(self):
        """Execute check and builtin diagnostics commands"""
        if self.check_cmd is not None:
            self._executed_cmd[" ".join(self.check_cmd)] = await exec_cmd(
                self.check_cmd
            )

        for diagnostic_cmd in self.diagnostics_cmds:
            self._executed_cmd[" ".join(diagnostic_cmd)] = await exec_cmd(
                diagnostic_cmd
            )

    @property
    def check_cmd(self):
        return self._fill_tmpl_cmd(self.check_metadata.Cli)

    @property
    def diagnostics_cmds(self) -> list[tuple[str]]:
        diagnostics_cmds = []
        for cmd in self.check_metadata.DiagnosticClis:
            diagnostic_cmd = self._fill_tmpl_cmd(cmd)
            if diagnostic_cmd is not None:
                diagnostics_cmds.append(diagnostic_cmd)

        return diagnostics_cmds

    @property
    def llm_summary(self) -> str:
        if self.passed:
            return "Explanation not needed."

        return super().llm_summary

    @property
    def passed(self):
        return self.status == "PASS"

    @property
    @abc.abstractmethod
    def display_object(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def display_row(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def object_id(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def object_name(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def unique_name(self) -> str:
        """Returns unique name of failed object"""

    @property
    @abc.abstractmethod
    def object_md(self) -> dict:
        """Returns object metadata"""


def _find_substrings(input_str) -> list[str]:
    # Regular expression pattern for matching substrings within double curly braces
    pattern = r"\{\{([^}]+)\}\}"
    matches = findall(pattern, input_str)
    return matches if len(matches) > 0 else []
