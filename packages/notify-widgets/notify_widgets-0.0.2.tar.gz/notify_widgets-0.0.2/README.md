# Description
This is a tool for displaying widgets showing custom info using a notification system.

![Example screenshot](Resources/screenshot.png)

# Getting Started
## Installation
Install with:
```sh
pip install git+https://codeberg.org/wime/tool-notify-widgets.git
```
Or from within a Python virtual environment:
```sh
pip install --user git+https://codeberg.org/wime/tool-notify-widgets.git
```


The tool is dependant on [mako](https://github.com/emersion/mako) being installed and used as the notification deamon.

## Usage
Use with:
```sh
notify-widgets -n {name}
```
or
```sh
python -m notify_widgets -n {name}
```

Options are:
* `-n` / `--name` -- Name of widget as defined in `config.toml`.
    - Required: `yes`
* `-a` / `--action` -- Action to trigger.
    - Options:
        * `run` -- Run widget.
        * `kill` -- Kill running process of widget.
        * `toggle` -- Toggle widget.
    * Default: `run`

# Configuration
The file `~/.config/notify-widgets/config.toml` is used for configuration. The file contains two sections `widgets` and `modules`.

## widgets
Each defined widget defines what and how the widget is displayed. Each widget is a contains of rows of modules. Each row can contain multiple modules.

Configuration options:
* `modules` {`list[list[str]]`} -- Rows of lists of modules. Each defined module must also be defines in the `modules` section.
    - Required: `yes`
* `vsep` {`str`} -- Vertical separator.
    - Default: `""`
* `hsep` {`str`} -- Horizontal separator (filled equal to the longest row).
    - Default: `""`

## modules
In this section the options for the different modules are defined. 

Configuration options:
* `icon` {`str`} -- Icon to be displayed.
* `icons_by_state {`dict[str, str]`} -- Icon to be displayed based on the given state.
* `icons_by_value` {`list[str]`} -- Icon based on value, from *low* to *high*. 
* `freq` {`int`} -- Update frequency in seconds.
    - Default: `1`
* `icon_in_line` {`bool`} -- If icon is placed in line with (`true`) or above (`false`) rest of module.
    - Default: `true`
* `new_line_indent` {`bool`} -- If all lines (if multiline) in the module should be indented similar to first line (due to icon). Should be used with `icon_in_line=true`.
    - Default: `false`

NOTE: The icon is set int the following priority:
1. If `icons_by_state` is given and the active state is in the given icons, this is the chosen icon.
2. If `icons_by_value` is given, this is the chosen icon.
3. If `icon` is given, this is the chosen icon.
4. Else: icon is `""`.

### Built-in modules
notify-widgets comes with some built-in modules:
* `modules.brightness`
* `modules.battery`
* `modules.network`
* `modules.audio`
* `modules.bluetooth`
* `modules.date`
* `modules.calendar`

### Custom modules
It is also possible to define cusotm modules. They need some additional configuration options:

* `exec` {`str`} -- Script to execute.
    - Required: `yes`
* `category` {`str`} -- What type of module this is.
    - Options:
	* `text` -- A purely text based module.
	* `percentage` -- A module with a percentage value.
	* `binary` -- A module with that is either `true` or `false` (on/off).
    - Default: `text`

The executable script needs to write a json object with one or more of the following keys:
* `text` {`str`} -- Text to be displayed.
* `value` {`float | bool`} -- A percentage value or a bool value.
* `state` {`str`} -- A state (muted, charging, etc.).

## Example config.toml
```toml
[widgets.system]
modules = [
	["network"],
	["battery", "custom/caffeine"],
	["brightness", "custom/nightlight"],
	["audio", "bluetooth"],
]
hsep = "   ¦   "
vsep = "- "

[modules.brightness]
icons_by_value = ["󰃞", "󰃟", "󰃠"]

[modules.battery]
icons_by_value = ["", "", "", "", ""]
icons_by_state = { charging = "" }

[modules.network]
icons_by_state = { wifi = "󰖩", disconnected = "󰖪", ethernet = "󰈀" }

[modules.audio]
icons_by_state = { muted = "", volume = "" }

[modules.bluetooth]
icon = ""
freq = 10

[modules."custom/nightlight"]
icon = ""
category = "binary"
exec = "python ~/.config/notify-widgets/modules/nightlight.py"

[modules."custom/caffeine"]
icon = ""
category = "binary"
exec = "python ~/.config/notify-widgets/modules/caffeine.py"
```

# Roadmap
* [ ] Publish on Pypi
* [ ] Make `network` module more advanced.
* [ ] Make it work with other notification deamons as well.

# License
The tool is published unther the MIT licens.
