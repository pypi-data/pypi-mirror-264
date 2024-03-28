import json
import subprocess

def get_shell_output(cmd: str) -> str:
    """
    Get output of shell command.

    Parameters
        cmd {str} -- Shell command to execute.
    Returns
        {str} Output from shell command.
    """
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.stdout.decode("utf-8")


def get_open_notifications():
    notifs = get_shell_output("makoctl list")
    notifs = json.loads(notifs)
    apps = [notif["app-name"]["data"] for notif in notifs["data"][0]]
    return apps


def dismiss_notification(app_name: str):
    try:
        id = {notif.app_name: notif.id for notif in get_open_notifications()}[app_name]
        subprocess.run(["makoctl", "dismiss", "-n", str(id)])
    except KeyError:
        return


def kill_notification(app_name: str) -> None:
    notifications = get_shell_output("makoctl list")
    notifications = json.loads(notifications)["data"][0]
    ids_by_names = {
        notif["app-name"]["data"]: notif["id"]["data"] for notif in notifications
    }
    notif_id = ids_by_names.get(app_name)
    if notif_id:
        subprocess.run(f"makoctl dismiss -n {notif_id}", shell=True)
