import pathlib
import shlex
import subprocess

from oak_cli.utils.logging import logger

INSTALL_PATH = pathlib.Path("~/.oak/argcomplete")


def handle_argcomplete() -> None:
    if not INSTALL_PATH.exists() or not any(INSTALL_PATH.iterdir()):
        INSTALL_PATH.mkdir(parents=True, exist_ok=True)
        cmd = f"activate-global-python-argcomplete -y --dest {INSTALL_PATH} --user"
        subprocess.check_call(shlex.split(cmd))
        logger.info(
            "To make sure command auto-completetion works please restart your terminal session"
        )
