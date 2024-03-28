import argparse
import os
import tomllib
import pathlib
from .modules import get_custom_module, get_default_module, DEFAULT
from .data_classes import Widget
from .utils import kill_notification, get_open_notifications



def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="widgets",
    )
    parser.add_argument("-a", "--action", default="run", required=False)
    parser.add_argument("-n", "--name", required=True)
    return parser.parse_args()


def get_config() -> dict:
    file = f"{os.getenv("HOME")}/.config/notify-widgets/config.toml"
    with open(file, "rb") as f:
        config = tomllib.load(f)
    return config


def run(app_name: str) -> None:
    config = get_config()
    all_modules = [] 
    for row in config["widgets"][app_name]["modules"]:
        modules = []
        for name in row:
            splitted_name = name.split("/")
            if splitted_name[0] == "custom":
                modules.append(get_custom_module(config=config["modules"][name]))
            else:
                if name not in DEFAULT:
                    continue
                modules.append(get_default_module(name=name, config=config["modules"][name]))
        all_modules.append(modules)
    widget = Widget(
        modules=all_modules,
        name=app_name,
        hsep=config["widgets"][app_name].get("hsep", " "),
        vsep=config["widgets"][app_name].get("vsep", ""),
    )
    widget.show()

def kill(app_name: str) -> None:
    kill_notification(app_name)

def toggle(app_name: str) -> None:
    if app_name in get_open_notifications():
        kill(app_name)
    else:
        run(app_name)


def main() -> None:
    args = get_args()
    actions = {
        "run": run,
        "kill": kill,
        "toggle": toggle,
    }
    if args.action in actions:
        try:
            actions[args.action](args.name)
        except FileNotFoundError:
            print("`~/.config/notify-widgets/config.toml` does not exist")

    
if __name__ == "__main__":
    main()
