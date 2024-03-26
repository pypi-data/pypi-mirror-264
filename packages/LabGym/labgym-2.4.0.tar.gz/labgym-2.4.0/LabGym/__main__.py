import json
from pathlib import Path
from urllib import request
from urllib.error import URLError

from packaging import version

from LabGym import __version__, gui


def main() -> None:
    """Check version and run LabGym."""

    try:
        current_version = version.parse(__version__)
        pypi_json = json.loads(request.urlopen("https://pypi.python.org/pypi/LabGym/json").read())
        latest_version = version.parse(pypi_json["info"]["version"])

        if latest_version > current_version:
            if "pipx" in str(Path(__file__)):
                upgrade_command = "pipx upgrade LabGym"
            else:
                upgrade_command = "python3 -m pip install --upgrade LabGym"

            print(f"You are using LabGym {current_version}, but version {latest_version} is available.")
            print(f"Consider upgrading LabGym by using the command '{upgrade_command}'.")
            print("For the details of new changes, check https://github.com/umyelab/LabGym.\n")
    except URLError:
        print("Unable to check for new versions of LabGym!")
        print("Please check https://github.com/umyelab/LabGym for updates.\n")


    gui.gui()


if __name__ == "__main__":
    main()
