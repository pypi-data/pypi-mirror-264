from datetime import datetime
import subprocess


def get_shell_output(cmd: str) -> str:
    output = subprocess.run(cmd, shell=True, capture_output=True)
    return output.stdout.decode("utf-8").rstrip("\n")


def get_brightness() -> dict[str, float]:
    value = get_shell_output("light")
    return {"value": float(value)}



def get_audio():
    result = get_shell_output("pactl list sinks")
    state = "volume"
    percent = 0.
    for item in result.split("\n"):
        try:
            key, value = item.strip("\t").replace("\n", "").split(": ", 1)
        except ValueError:
            pass
        else:
            if key == "Volume":
                percent = float(value.split("/")[1][1:-2].replace(",", "."))
            elif key == "Mute":
                state = {"yes": "muted", "no": "volume"}[value]
            # elif key == "Description":
            #     description = value
    if state == "muted":
        percent = 0.
    return {"value": percent, "state": state}


def get_bluetooth():
    result = get_shell_output("bluetoothctl show")
    for item in result.split("\n"):
        try:
            key, value = item.lstrip("\t").replace("\n", "").replace(" ", "").split(":", 1)
        except ValueError:
            pass
        else:
            if key == "Powered":
                state = {"yes": True, "no": False}[value]
                return {"value": state}
    return {}


def get_battery():
    result = get_shell_output("upower -i /org/freedesktop/UPower/devices/battery_BAT0")
    battery_dict = {}
    for values in result.split("\n"):
        dict_input = values.replace(" ", "").replace("\n", "").split(":")
        if len(dict_input) == 2:
            battery_dict[dict_input[0]] = dict_input[1]
    state = battery_dict["state"]
    state = {"pending-charge": "charging"}.get(state, state)
    percent = int(round(float(battery_dict["percentage"][:-1].replace(",", "."))))
    return {"value": percent, "state": state} 


def get_wifi():
    """Get wifi connection."""
    connection = get_shell_output("nmcli con show --active")
    if not connection:
        return {"state": "disconnected", "text": "N/A"}
    return {"state": "wifi", "text": connection.split("\n")[1].split(" ")[0]}


def get_calendar() -> dict:
    cal = get_shell_output("cal -w").rstrip(" ").rstrip("\n")
    lines = []
    for i, line in enumerate(cal.split("\n")):
        if i == 0:
            # lines.append(f"{line.strip(" ")}")
            pass
        elif i == 1:
            lines.append(f" w |{line[2:]}")
        else:
            lines.append(f"{line[:2]} |{line[2:]}") 
    cal = "\n".join(lines)
    translator = {
        "ma": "mo",
        "ti": "tu",
        "on": "we",
        "to": "th",
        "lø": "sa",
        "sø": "su"
    }
    for key, value in translator.items():
        cal = cal.replace(key, value)
    current_month = datetime.now().strftime("%B %Y")

    return {"text": f"{current_month}\n{cal}"}


def get_date() -> dict:
    return {"text": datetime.now().strftime("%e. %B %Y")}

