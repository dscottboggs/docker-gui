"""Miscellaneous functions.

All code in this file should be purely functional.
"""

from subprocess import run, PIPE
from subprocess import CompletedProcess
from os.path import isdir
from os import access
from os import F_OK as file_exists
from os import makedirs as mkdir


def runcmd(cmd: str) -> CompletedProcess:
    """Alias subprocess.run, with check, shell, stdin and stdout enabled."""
    return run(cmd, check=True, shell=True, stdout=PIPE, stdin=PIPE)


def check_isdir(filepath: str) -> bool:
    """Check to make sure a particular filepath is a directory.

    Also check that it's not a file and create it if it doesn't already
    exist.
    """
    if not isdir(filepath):
        if access(filepath, mode=file_exists):
            raise FileExistsError(
                "Goal directory %s exists as a file." % (filepath)
            )
        else:
            mkdir(filepath, mode=0o755)
            return True
    return False
