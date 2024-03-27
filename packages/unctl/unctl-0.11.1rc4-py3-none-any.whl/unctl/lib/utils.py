import asyncio
import contextlib
import subprocess


UNSET = object()


class GlobalVar:
    _VARIABLES = set()

    def __init__(self, name, default=UNSET, allow_overrides=True):
        self.name = name
        self.default = default
        self._current = UNSET
        self.allow_overrides = allow_overrides
        self._variable_set = False

    @classmethod
    def make(cls, name, *, default=UNSET, allow_overrides=True):
        if name in cls._VARIABLES:
            raise ValueError(f"Variable {name} already defined.")
        cls._VARIABLES.add(name)
        return cls(name, default=default, allow_overrides=allow_overrides)

    def set(self, value):
        if self._variable_set and not self.allow_overrides:
            raise ValueError(
                f"Cannot set variable {self.name}, as overrides "
                f"isn't allowed for this variable."
            )
        self._variable_set = True
        self._current = value

    def get(self):
        if self._current is not UNSET:
            return self._current
        elif self.default is not UNSET:
            return self.default
        raise LookupError(f"Variable '{self.name}' is unset.")

    @contextlib.contextmanager
    def context(self, new):
        old = self.get()
        try:
            self.set(new)
            yield
        finally:
            self.set(old)


async def exec_cmd(cmd: str | tuple[str]):
    if not cmd:
        return

    command = cmd

    if isinstance(command, tuple) and len(cmd) == 1:
        # common normalization after template parsing
        command = command[0]

    if isinstance(command, str):
        command = command.split()

    proc = await asyncio.create_subprocess_exec(
        *command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    stdout, stderr = await proc.communicate()

    if stderr:
        decoded_stderr = stderr.decode("utf-8")
        print(f"Error(executing command({cmd}) stderr: {decoded_stderr}")
        return f"stderr: {decoded_stderr}"

    return stdout.decode("utf-8")
