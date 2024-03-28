import json
import os
import subprocess
from typing import Callable, Literal

from .data_classes import Module, PercentageState, TextState, BinaryState
from .default_modules import *


DEFAULT = {
        "audio": {"fun": get_audio, "category": "percentage"},
        "battery": {"fun": get_battery, "category": "percentage"},
        "network": {"fun": get_wifi, "category": "text"},
        "brightness": {"fun": get_brightness, "category": "percentage"},
        "calendar": {"fun": get_calendar, "category": "text"},
        "date": {"fun": get_date, "category": "text"},
        "bluetooth": {"fun": get_bluetooth, "category": "binary"}
        # "calendar": ...,
} 

CONTAINERS = {
        "percentage": PercentageState,
        "text": TextState,
        "binary": BinaryState,
}


def shell_to_fun(cmd: str) -> Callable:
    cmd = cmd.replace("~", os.environ["HOME"])
    cmd = cmd.replace("$HOME", os.environ["HOME"])
    def fun() -> dict:
        output = subprocess.run(cmd, shell=True, capture_output=True)
        return json.loads(output.stdout.decode("utf-8").rstrip("\n"))
    return fun


def get_module(
    config: dict,
    fun: Callable,
    category: Literal["percentage", "text", "binary"]
) -> Module:
    state_container = CONTAINERS[category](
        icon=config.get("icon", ""),
        icons_by_state=config.get("icons_by_state"),
        icons_by_value=config.get("icons_by_value"),
        icon_in_line=config.get("icon_in_line", True),
        new_line_indent=config.get("new_line_indent", False)
    )
    return Module(fun=fun, state=state_container, freq=config.get("freq", 1))


def get_default_module(name: str, config: dict) -> Module:
    """Get default module."""
    return get_module(
        config=config,
        fun=DEFAULT[name]["fun"],
        category=DEFAULT[name]["category"]
    )


def get_custom_module(config: dict) -> Module:
    """Get custom module."""
    return get_module(
        config=config,
        fun=shell_to_fun(cmd=config.get("exec", "")),
        category=config.get("category", "text")
    )
