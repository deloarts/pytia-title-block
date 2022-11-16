"""
    Constants for the pytia title block app.
"""

import os

__version__ = "0.2.1"

PYTIA = "pytia"
PYTIA_TITLE_BLOCK = "pytia_title_block"

APP_NAME = "PYTIA Title Block"
APP_VERSION = __version__

LOGON = str(os.environ.get("USERNAME"))
CNEXT = "win_b64\\code\\bin\\CNEXT.exe"
TEMP = str(os.environ.get("TEMP"))
APPDATA = f"{str(os.environ.get('APPDATA'))}\\{PYTIA}\\{PYTIA_TITLE_BLOCK}"
LOGS = f"{APPDATA}\\logs"
LOG = "app.log"
PID = os.getpid()
PID_FILE = f"{TEMP}\\{PYTIA_TITLE_BLOCK}.pid"
VENV = f"\\.env\\{APP_VERSION}"
VENV_PYTHON = VENV + "\\Scripts\\python.exe"
VENV_PYTHONW = VENV + "\\Scripts\\pythonw.exe"
PY_VERSION = APPDATA + "\\pyversion.txt"

PROP_DRAWING_PATH = "pytia.drawing_path"

CONFIG_APPDATA = "config.json"
CONFIG_SETTINGS = "settings.json"
CONFIG_DEPS = "dependencies.json"
CONFIG_DEPS_DEFAULT = "dependencies.default.json"
CONFIG_PROPS = "properties.json"
CONFIG_PROPS_DEFAULT = "properties.default.json"
CONFIG_TB_ITEMS = "title_block_items.json"
CONFIG_TB_ITEMS_DEFAULT = "title_block_items.default.json"
CONFIG_INFOS = "information.json"
CONFIG_INFOS_DEFAULT = "information.default.json"
CONFIG_USERS = "users.json"

TOLERANCE_TABLE_NAME = "tolerance_table"
TOLERANCE_TABLE_CELL_HEIGHT = 4.5
TOLERANCE_TABLE_CELL_WIDTH = 32.3333

WEB_PIP = "www.pypi.org"
