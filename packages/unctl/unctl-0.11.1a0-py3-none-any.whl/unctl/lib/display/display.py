import os
import re
from collections import defaultdict
from typing import List, Dict

from colorama import init, Fore, Style
from prettytable import PrettyTable
from unctl.config.config import get_config_instance

from unctl.constants import CheckProviders
from unctl.lib.display.tables.base import BaseTable
from unctl.lib.display.tables.constants import TableNames
from unctl.lib.models.checks import CheckMetadataModel

init(autoreset=True)


class Displays:
    DISPLAYS = {}

    def __init_subclass__(cls, **kwargs):
        try:
            cls.DISPLAYS[kwargs["name"]] = cls
        except KeyError:
            pass

    @classmethod
    def get_display(cls, name):
        return cls.DISPLAYS[name]


class Display(Displays):
    """Handles display-related functionalities."""

    PROVIDER = None
    DISPLAY_NAME = None

    term_width = 80
    options = None

    _current_progress = 0
    _total = 1

    @classmethod
    def init(cls):
        """Displays the results of the checks in a formatted table."""
        # Initialize colorama for terminal colored output
        init(autoreset=True)

        # Calculate terminal width for dynamic UI formatting
        try:
            cls.term_width = os.get_terminal_size().columns
        except OSError:
            # in case output won't go to the terminal
            cls.term_width = 200

    @staticmethod
    def create_default_table(field_names, align):
        fmt_fields = []
        for field_name in field_names:
            fmt_fields.append(
                Fore.LIGHTBLUE_EX + Style.BRIGHT + field_name + Style.RESET_ALL
            )

        table = PrettyTable(fmt_fields)
        table.horizontal_char = "─"
        table.vertical_char = "|"
        table.junction_char = "─"
        table.border = True
        table.frame = True
        table.align = align

        return table

    @staticmethod
    def find_substrings(input_str):
        """Find substrings wrapped in double curly braces in a given string."""
        pattern = r"\{\{([^}]+)\}\}"
        matches = re.findall(pattern, input_str)
        return matches if matches else None

    @classmethod
    def init_progress_bar(cls, total_count: int):
        cls._total = total_count
        # Display the progress bar header
        pbar_message = f"Running {cls.DISPLAY_NAME} Checks"
        print(
            f"\n{Fore.YELLOW}{Style.BRIGHT}" f"{'─' * cls.term_width}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.YELLOW}"
            f"{Style.BRIGHT}"
            f"{pbar_message.center(cls.term_width)}"
            f"{Style.RESET_ALL}"
        )
        print(
            f"{Fore.YELLOW}"
            f"{Style.BRIGHT}"
            f"{'─' * cls.term_width}"
            f"{Style.RESET_ALL}"
            f"\n"
        )

    @classmethod
    async def progress_bar_callback(cls, check, reports):
        cls.increment_progress_bar(check.CheckTitle)
        print()

    @classmethod
    def increment_progress_bar(cls, check_name, bar_length=80):
        """Displays a progress bar with the specified percentage completion."""

        cls._current_progress += 1
        percentage = cls._current_progress / cls._total

        blocks = int(round(bar_length * percentage))
        block_char = "▶"

        if percentage < 1:
            filled_part = Fore.LIGHTRED_EX + block_char * blocks + Style.RESET_ALL
            percent_color = Fore.LIGHTRED_EX
        else:
            filled_part = Fore.LIGHTGREEN_EX + block_char * blocks + Style.RESET_ALL
            percent_color = Fore.LIGHTGREEN_EX

        empty_part = " " * (bar_length - blocks)
        progress_string = (
            f"\r{Fore.BLUE + Style.BRIGHT}In progress: {check_name}{Style.RESET_ALL}  "
            f"|{filled_part + empty_part}| "
            f"{percent_color + Style.BRIGHT}{percentage * 100:.1f}%{Style.RESET_ALL}"
        )
        # Move the cursor up by one line and then clear that line
        move_up_and_clear_line = (
            f"\033[A"  # Move up one line
            f"\r{' ' * (cls.term_width - 1)}"  # Clear the line
            f"\r"  # Move cursor to the beginning of the line again
        )
        print(move_up_and_clear_line, end="", flush=True)

        print(progress_string, end="", flush=True)

    @staticmethod
    def pad_content(content, width):
        """Pad content to given width."""
        content_length = len(content)
        if content_length < width:
            padding = " " * (width - content_length)
            return content + padding
        return content

    @staticmethod
    def center_content(content, width):
        """Center the content for given width."""
        return content.center(width)

    @classmethod
    def _get_sorted_table(cls, table_name, table, results, llm_summary=False):
        builder = BaseTable.get_table_builder_for(cls.PROVIDER, table_name=table_name)
        table = builder.configure(
            results,
            context={"llm_summary": llm_summary},
            initial_table=table,
            display=cls,
            divider=True,
        ).build()

        # Color the headers in blue
        table_string = table.get_string()
        for field_name in table.field_names:
            # Use exact match by adding word boundaries \b
            exact_match_pattern = r"\b{}\b".format(re.escape(field_name))

            # Replace the exact match of field_name with color formatting
            table_string = re.sub(
                exact_match_pattern,
                Fore.LIGHTBLUE_EX + Style.BRIGHT + field_name + Style.RESET_ALL,
                table_string,
                1,
            )
        return table_string

    @classmethod
    def display_sort_by_check_table(cls, check_details, llm_summary=False):
        """Display per check table."""
        table = PrettyTable()

        # Set the table appearance to use solid lines for borders
        table.horizontal_char = "─"
        table.vertical_char = "|"
        table.junction_char = "─"
        table.border = True
        table.frame = True
        check_details = [detail for detail in check_details if detail.status == "FAIL"]
        table = cls._get_sorted_table(
            TableNames.SORTED_BY_CHECKS, table, check_details, llm_summary
        )
        print(table)

    @classmethod
    def display_list_checks_table(cls, checks: List[CheckMetadataModel]):
        print()

        table = PrettyTable()

        # Set table appearance to use solid lines for borders
        table.horizontal_char = "─"
        table.vertical_char = "|"
        table.junction_char = "─"
        table.border = True
        table.frame = True

        builder = BaseTable.get_table_builder_for(
            cls.PROVIDER, table_name=TableNames.LIST_CHECKS
        )
        table = builder.configure(
            checks, initial_table=table, display=cls, divider=True
        ).build()

        table_string = table.get_string()
        for field_name in table.field_names:
            table_string = table_string.replace(
                field_name,
                Fore.LIGHTBLUE_EX + Style.BRIGHT + field_name + Style.RESET_ALL,
                1,
            )
        print(table_string)

    @classmethod
    def display_grouped_data(cls, name: str, data: Dict[str, int]):
        table = cls.create_default_table([name, "Checks Count"], "l")

        for item, count in sorted(data.items()):
            table.add_row(
                [
                    item,
                    count,
                ],
            )

        print(table.get_string())

    @staticmethod
    def organize_results_by_check(results):
        """Organize results by CheckTitle."""
        organized_results = defaultdict(list)
        for check_name, checks in results.items():
            for result in checks:
                check_title = result.check_metadata.CheckTitle
                organized_results[check_title].append(result)
        return organized_results

    @classmethod
    def display_sortby_object(cls, results, llm_summary):
        results = sum(results.values(), [])
        table = PrettyTable()
        # Set the table appearance to use solid lines for borders
        table.horizontal_char = "─"
        table.vertical_char = "|"
        table.junction_char = "─"
        table.border = True
        table.frame = True

        config = get_config_instance()
        if config.filter.failed_only:
            results = [result for result in results if result.status == "FAIL"]

        table_string = cls._get_sorted_table(
            TableNames.SORTED_BY_OBJECT, table, results, llm_summary
        )
        table_output = (
            table_string.replace(
                "FAIL", Fore.RED + Style.BRIGHT + "FAIL" + Style.RESET_ALL
            )
            .replace("PASS", Fore.GREEN + Style.BRIGHT + "PASS" + Style.RESET_ALL)
            .replace(
                "Critical",
                Fore.LIGHTRED_EX + Style.BRIGHT + "Critical" + Style.RESET_ALL,
            )
            .replace(
                "Severe",
                Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "Severe" + Style.RESET_ALL,
            )
            .replace(
                "High",
                Fore.LIGHTYELLOW_EX + Style.BRIGHT + "High" + Style.RESET_ALL,
            )
            .replace("Low", Fore.LIGHTGREEN_EX + Style.BRIGHT + "Low" + Style.RESET_ALL)
        )
        print(table_output)

    @classmethod
    def display_sortby_check(cls, results, llm_summary):
        organized_results = cls.organize_results_by_check(results)
        for check_title, check_details in organized_results.items():
            statuses = [detail.status for detail in check_details]

            # Skip the check if failed only is enabled and all checks passed.
            config = get_config_instance()
            if config.filter.failed_only and all(
                status == "PASS" for status in statuses
            ):
                continue

            if all(status == "PASS" for status in statuses):
                print(Fore.WHITE + Style.BRIGHT + Fore.GREEN + f"✅ {check_title}")
                print()
            else:
                print(Fore.WHITE + Style.BRIGHT + Fore.RED + f"❌ {check_title}")
                cls.display_sort_by_check_table(check_details, llm_summary)
                print()

    @classmethod
    def display_results_table(cls, results, llm_summary=False, sort_by="object"):
        """Displays the results of the checks in a formatted table."""
        term_width = cls.term_width

        print("\n" + Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL)
        print(
            f"{Fore.YELLOW}"
            f"{Style.BRIGHT}"
            f"{'Checks Scan Report'.center(term_width)}"
            f"{Style.RESET_ALL}"
        )
        print(Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL + "\n")
        print()
        if sort_by == "object":
            cls.display_sortby_object(results, llm_summary)
        elif sort_by == "check":
            cls.display_sortby_check(results, llm_summary)
        print("\n" + Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL)
        print(
            f"{Fore.YELLOW}"
            f"{Style.BRIGHT}"
            f"{'End of Scan Report'.center(term_width)}"
            f"{Style.RESET_ALL}"
        )
        print(Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL + "\n")
        print()

    @staticmethod
    def debug_results_structure(results):
        unique_combinations = set()

        for result in results:
            sub_service = result.check_metadata.SubServiceName
            check_title = result.check_metadata.CheckTitle

            unique_combinations.add((sub_service, check_title))

        for combo in unique_combinations:
            print(combo)


class K8SDisplay(Display, name=CheckProviders.K8S):
    PROVIDER = CheckProviders.K8S
    DISPLAY_NAME = "Kubernetes"


class MySQLDisplay(Display, name=CheckProviders.MySQL):
    PROVIDER = CheckProviders.MySQL
    DISPLAY_NAME = "MySQL"
