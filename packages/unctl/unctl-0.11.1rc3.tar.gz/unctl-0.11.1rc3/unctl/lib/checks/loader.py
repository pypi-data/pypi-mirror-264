import importlib
import sys
from typing import Optional

from unctl.config.app_config import AppConfig
from unctl.lib.checks.check import Check
from unctl.list import load_checks


class ChecksLoader:
    """
    Gathers all the checks from the checks directory
    """

    def __init__(self, checks_dir="checks"):
        self.checks_dir = checks_dir

    def _load_check_module(self, module_name):
        module = importlib.import_module(module_name)
        return module

    def load_all(self, provider, config: Optional[AppConfig] = None):
        checks_modules = load_checks(
            provider=provider,
            checks_dir=self.checks_dir,
            config=config,
        )

        checks: list[Check] = []
        for module_name in checks_modules:
            module = self._load_check_module(module_name)

            # Load only the checks
            if module.__package__ is None or len(module.__package__.split(".")) < 4:
                continue

            # Extract class name from the module's file name
            class_name = module.__package__.split(".")[-1]

            # Instantiate the class named after the module
            check_class = getattr(module, class_name)

            # load the class
            check_instance = check_class()

            # Ensure that the execute method exists in the check class
            if hasattr(check_instance, "execute"):
                checks.append(check_instance)

        if len(checks) > 0:
            print(f"✅ Loaded {len(checks)} check(s)")
        else:
            sys.exit("❌ No checks loaded")

        return checks
