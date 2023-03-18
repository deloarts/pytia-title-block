"""
    Explorer submodule for the tools menu bar.
"""

import os
import subprocess
from pathlib import Path

from const import EXPLORER


def explorer(path: Path) -> None:
    """Opens the file explorer at the given path."""
    if os.path.isdir(path):
        subprocess.run([EXPLORER, path])
    elif os.path.isfile(path):
        subprocess.run([EXPLORER, "/select,", path])
