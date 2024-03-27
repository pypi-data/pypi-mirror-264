import asyncio
import inspect
from typing import Awaitable, Callable, Optional

from unctl.config.app_config import AppConfig
from unctl.lib.checks.loader import ChecksLoader
from unctl.lib.collectors.base import DataCollector
from unctl.analytics import CheckRunEvent, track_json_error
import rich
from pydantic import ValidationError
from unctl.config.config import EMPTY_CONFIG

from unctl.lib.checks.check import Check
from unctl.lib.checks.check_report import CheckReport
from unctl.lib.llm.instructions import GROUP, INSTRUCTIONS
from unctl.lib.llm.session import LLMSessionKeeper
from unctl.lib.models.recommendations import GroupLLMRecommendation
from unctl.lib.models.remediations import FailureGroup


# Main Application

OnCheckCompleteCallback = Callable[[Check, list[CheckReport]], Awaitable[None]]


class CollectDataError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ResourceChecker:
    _check_reports: dict[str, list[CheckReport]]
    _failure_groups: list[FailureGroup]

    def __init__(
        self,
        provider: str,
        config: Optional[AppConfig] = None,
    ):
        collector = DataCollector.make_collector(provider)
        self._collector = collector
        self._provider = provider
        self._config = config if config is not None else EMPTY_CONFIG

        loader = ChecksLoader()
        checks = loader.load_all(provider=provider, config=self._config)
        self._checks = checks

        self._check_reports = {}
        self._failure_groups = []

    @property
    def checks(self):
        return self._checks

    async def execute(
        self,
        on_check_complete: Optional[OnCheckCompleteCallback] = None,
    ) -> dict[str, list[CheckReport]]:
        """
        Execute checks agaist provider's resources.

        Args:
            on_check_complete (Optional[OnCheckCompleteCallback], optional):
            Will be called after completion of each check.
            Passing the check and it's results. Defaults to None.

            Example usage:
            ```
            async def custom_callback(check: Check, reports: List[CheckReport]):
                # Your logic here

            await app.execute(on_check_complete=custom_callback)
            ```

        Returns:
            dict[str, list[CheckReport]]: A dictionary mapping check IDs
            to their corresponding lists of check reports.
        """

        data = await self._collector.fetch_data(self._config)
        if data is None:
            raise CollectDataError("Failed to collect inventory")

        print(f"✅ Collected {self._provider} data")

        ignored_objects = self._config.ignore.objects

        for check in self._checks:
            check_event = CheckRunEvent()
            if check.Enabled is False:
                continue
            # todo: remove this once all checks are async
            check_reports = (
                await check.execute(data)
                if inspect.iscoroutinefunction(check.execute)
                else check.execute(data)
            )
            failed_count = sum(1 for report in check_reports if not report.passed)
            # Track event: Check name, failed count, and execution time
            check_event.send(check.CheckID, failed_count)

            # filter ignored objects
            filtered_check_reports = list(
                report
                for report in check_reports
                if (
                    report.object_name not in ignored_objects
                    or (
                        len(ignored_objects[report.object_name]) > 0
                        and check.CheckID not in ignored_objects[report.object_name]
                    )
                )
            )

            self._check_reports[check.CheckID] = filtered_check_reports

            if on_check_complete is not None:
                await on_check_complete(check, filtered_check_reports)

        return self._check_reports

    async def diagnose(self):
        # TODO: could use concurrency here
        for check, reports in self._check_reports.items():
            for report in reports:
                if not report.passed:
                    await report.execute_diagnostics()

    async def analyze_results(self):
        batch_size = 10
        failing_items = self.failing_reports
        total_tasks = len(failing_items)
        for batch_start in range(0, total_tasks, batch_size):
            batch_end = min(batch_start + batch_size, total_tasks)
            tasks = [
                self._analyze_result(report=failed_item)
                for failed_item in failing_items[batch_start:batch_end]
            ]
            await asyncio.gather(*tasks)

    async def _analyze_result(self, report: CheckReport):
        # start an assisted troubleshooting session
        await report.init_llm_session()
        await report.get_next_steps()
        await report.log_recommendation(self.failing_objects)

        return report

    def _find_related_group(self, related_objects: list[str]):
        for group in self._failure_groups:
            for object in related_objects:
                if group.contains_object(object):
                    return group

    async def _append_to_existing_group(
        self,
        failure_report: CheckReport,
        group: FailureGroup,
        recommendation: GroupLLMRecommendation,
        related_reports: list[CheckReport],
    ):
        for related in related_reports:
            not_in_group = not group.contains_object(related.unique_name)

            if related.unique_name != failure_report.unique_name or not_in_group:
                for output in related.cmd_output_messages:
                    await group.session.push_info(output)

            if not_in_group:
                group.objects.append(related)
                print(f"\t❌ Added <{related.object_name}> to group <{group.title}>")

        recommendation = await self._request_group_recommendation(
            message=(
                "Provide complete analysis on provided data for all related objects.\n"
                "Figure out possible root cause.\n"
                "Sort object list from root causes to downstream failures."
            ),
            session=group.session,
        )

        if recommendation is None:
            return

        related_reports = group.objects.copy()

        related_reports = sorted(
            related_reports,
            key=lambda report: (
                group.objects.index(report.unique_name)
                if report.unique_name in group.objects
                else float("inf")
            ),
        )

        if group.title != recommendation.title:
            rich.print(
                f"\t⏩ Updated group context <{group.title}> ➱ "
                f"<{recommendation.title}>\n"
                f"\t[bold yellow]Summary:[/bold yellow] {group.summary}\n"
            )

        group.title = recommendation.title
        group.summary = recommendation.summary
        group.objects = related_reports

    async def _create_new_group(
        self,
        failure_report: CheckReport,
        session: LLMSessionKeeper,
        recommendation: GroupLLMRecommendation,
        related_reports: list[CheckReport],
    ):
        for related in related_reports:
            if related.unique_name != failure_report.unique_name:
                for output in related.cmd_output_messages:
                    await session.push_info(output)

        # request additional analysis only if found more that 1 object related to issue
        if len(related_reports) > 1:
            recommendation = await self._request_group_recommendation(
                message=(
                    "Provide complete analysis on provided data "
                    "for all related objects.\n"
                    "Figure out possible root cause.\n"
                    "Sort object list from root causes to downstream failures."
                ),
                session=session,
            )

            if recommendation is None:
                return

        self._failure_groups.append(
            FailureGroup(
                id=(
                    f"{failure_report.unique_name}"
                    f"-{failure_report.check_metadata.CheckID}"
                ),
                title=recommendation.title,
                summary=recommendation.summary,
                objects=related_reports,
                session=session,
            )
        )

        rich.print(
            f"❌ Created group for check <{failure_report.check_metadata.CheckTitle}> "
            f"and object <{failure_report.object_name}>\n"
            f"[bold yellow]Title:[/bold yellow] {recommendation.title}\n"
            f"[bold yellow]Summary:[/bold yellow] {recommendation.summary}\n"
            f"[bold yellow]Objects:[/bold yellow] {', '.join(recommendation.objects)}\n"
        )

    async def _find_report_deps(
        self, failure_report: CheckReport, failing_reports: list[CheckReport]
    ):
        session = LLMSessionKeeper()
        await session.init_session(data=failure_report.cmd_output_messages)

        group = await self._request_group_recommendation(
            message=(
                "Identify possible related objects only from "
                f"the pool: {', '.join(self.failing_objects)}.\n"
                "Related objects may be mentioned (even if partially) "
                "in the logs, error events, etc "
                f"and which may be possibly impacted by {failure_report.unique_name}"
            ),
            session=session,
        )

        related_reports = [
            report for report in failing_reports if report.unique_name in group.objects
        ]

        if failure_report.unique_name not in group.objects:
            related_reports.append(failure_report)

        existing_group = self._find_related_group(related_objects=group.objects)
        if existing_group is not None:
            session = existing_group.session

        if existing_group is not None:
            await self._append_to_existing_group(
                failure_report=failure_report,
                group=existing_group,
                recommendation=group,
                related_reports=related_reports,
            )
        else:
            await self._create_new_group(
                failure_report=failure_report,
                session=session,
                recommendation=group,
                related_reports=related_reports,
            )

        return related_reports

    async def find_dependencies(self):
        print("🔀 Looking for dependencies between failures...\n")

        leftovers = self.failing_objects.copy()
        failing_reports = self.failing_reports.copy()

        for failure_report in failing_reports:
            if failure_report.unique_name not in leftovers:
                continue

            failing_reports = list(
                report for report in failing_reports if report.unique_name in leftovers
            )
            related_reports = await self._find_report_deps(
                failure_report=failure_report, failing_reports=failing_reports
            )

            for related in related_reports:
                if related.unique_name in leftovers:
                    leftovers.remove(related.unique_name)

    async def _request_group_recommendation(
        self, message: str, session: LLMSessionKeeper
    ):
        try:
            recommendation = await session.request_llm_recommendation(
                message=message,
                instructions=INSTRUCTIONS[self._provider][GROUP],
                polling_timeout=1,
            )

            return GroupLLMRecommendation.model_validate_json(recommendation)
        except ValidationError as e:
            print(f"Failed to parse group recommendation for {id}")
            track_json_error("ValidationError", str(e), "GroupLLMRecommendation")
            return GroupLLMRecommendation()

    @property
    def failing_reports(self) -> list[CheckReport]:
        failing = []
        for check_list in self._check_reports.values():
            failing.extend(item for item in check_list if not item.passed)

        return failing

    @property
    def failing_objects(self):
        items = self.failing_reports
        objects = list(set(item.unique_name for item in items))
        return objects

    @property
    def reports(self):
        return self._check_reports

    @property
    def failure_groups(self):
        groups = [item for item in self._failure_groups if item.failed_count > 1]
        other = [
            item.objects[0] for item in self._failure_groups if item.failed_count == 1
        ]
        sorted_groups = sorted(groups, key=lambda item: item.failed_count, reverse=True)

        sorted_groups.append(
            FailureGroup(
                id="other",
                title="Other",
                summary=(
                    "This group contains all the failures which "
                    "are not related to any other problem."
                ),
                objects=other,
                session=None,
            )
        )

        return sorted_groups
