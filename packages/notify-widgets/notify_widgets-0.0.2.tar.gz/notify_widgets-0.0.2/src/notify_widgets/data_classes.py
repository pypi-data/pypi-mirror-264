from dataclasses import dataclass, field
import json
import threading
import time
from typing import Callable
import subprocess

from .utils import get_open_notifications, get_shell_output


@dataclass
class State:
    icon: str = ""
    icons_by_state: dict[str, str] | None = None
    icons_by_value: list[str] | None = None
    icon_in_line: bool = True
    new_line_indent: bool = False

    def __post_init__(self) -> None:
        self._value: bool | float | None = None
        self._state: str | None = None
        self._text: str = ""

    @property
    def value(self) -> bool | float | None:
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value
        self.set_icon()

    @property
    def state(self) -> str | None:
        return self._state

    @state.setter
    def state(self, value) -> None:
        self._state = value
        self.set_icon()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value) -> None:
        self._text = value
        self.set_icon()

    def set_icon(self) -> None:
        """Set icon based on given arguments"""
        if self.icons_by_state and self.state:
            self.icon = self.icons_by_state.get(self.state, "")


class PercentageState(State):
    def set_icon(self) -> None:
        """Set icon based on given arguments"""
        if self.icons_by_state and self.state:
            self.icon = self.icons_by_state.get(self.state, "")
            if self.icon:
                return
        if self.icons_by_value and self.value:
            num_values = len(self.icons_by_value)
            multiplier = 100 / (num_values - 1)
            values = [multiplier * x for x in range(num_values)]
            temp_value = min(values, key=lambda x:abs(x-self.value))
            index = values.index(temp_value)
            self.icon = self.icons_by_value[index]

    def __repr__(self) -> str:
        if self.value is None:
            return ""
        percentage = int(round(self.value))
        icon = f"{self.icon:<3}"
        if not self.icon_in_line:
            icon += "\n"
        else:
            icon += " "
        return f"{icon}{percentage:>3}%"


class BinaryState(State):
    def set_icon(self) -> None:
        """Set icon based on given arguments"""
        if self.icons_by_state and self.state:
            self.icon = self.icons_by_state.get(self.state, "")
            if self.icon:
                return
        if self.icons_by_value and self.value:
            self.icon = self.icons_by_value[int(self.value)]

    def __repr__(self) -> str:
        if self.value is None:
            return ""
        toggles = {True: " ", False: " "}
        icon = f"{self.icon:<3}"
        if not self.icon_in_line:
            icon += "\n"
        else:
            icon += " "
        return f"{icon}{toggles[bool(self.value)]:>4}"


class TextState(State):
    def __repr__(self) -> str:
        if not self.text:
            return ""
        icon = self.icon
        if self.icon:
            icon = f"{self.icon:<3}"
        text = self.text
        if not self.icon_in_line:
            icon += "\n"
        elif not self.icon:
            pass
        else:
            icon += "  "
        if self.new_line_indent:
            lines = self.text.split("\n")
            lines = [f"{"":^3}  {line}" if i > 0 else line for i, line in enumerate(lines)]
            text = "\n".join(lines)
        return f"{icon}{text}"


@dataclass
class Module:
    fun: Callable
    state: State
    freq: int = 1
    content: str = field(init=False)
    keep_going: bool = True

    def __repr__(self) -> str:
        return str(self.state)

    def thread(self) -> None:
        while self.keep_going:
            try:
                content = self.fun()
                self.state.value = content.get("value")
                self.state.state = content.get("state")
                self.state.text = content.get("text")
            except Exception:
                pass
            time.sleep(self.freq)

    def run(self) -> None:
        x = threading.Thread(target=self.thread)
        x.start()


@dataclass
class Widget:
    modules: list[list[Module]]
    name: str
    hsep: str = "|"
    vsep: str = ""

    def __repr__(self) -> str:
        lines = []
        for row in self.modules:
            lines.append(f" {self.hsep} ".join([str(module) for module in row]))
        longest_line = len(max("\n".join(lines).split("\n"), key=len))
        if self.vsep:
            vsep = f"{self.vsep}" * int(longest_line / len(self.vsep)) + "\n"
        else:
            vsep = ""
        return f"\n{vsep}".join(lines)

    def notify_send(self):
        subprocess.run(
            [
                "notify-send",
                str(self),
                "-a",
                self.name,
                "-h",
                "string:x-canonical-private-synchronous:sys-notify"
            ]
        )
    
    @property
    def is_active(self) -> bool:
        open_notifications = get_open_notifications()
        return self.name in open_notifications

    def kill_modules(self) -> None:
        for row in self.modules:
            for module in row:
                module.keep_going = False

    def show(self):
        for row in self.modules:
            for module in row:
                module.run()
        keep_going = True
        while keep_going:

            self.notify_send()
            try:
                self.notify_send()
            except Exception:
                pass
            time.sleep(1)
            if not self.is_active:
                keep_going = False
                self.kill_modules()
