"""
    Loads the content from config files.

    Important: Do not import third party modules here. This module
    must work on its own without any other dependencies!
"""

import atexit
import importlib.resources
import json
import os
import tkinter.messagebox as tkmsg
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from pathlib import Path
from typing import List
from typing import Optional

from const import APP_VERSION
from const import APPDATA
from const import CONFIG_APPDATA
from const import CONFIG_INFOS
from const import CONFIG_INFOS_DEFAULT
from const import CONFIG_PROPS
from const import CONFIG_PROPS_DEFAULT
from const import CONFIG_SETTINGS
from const import CONFIG_TB_ITEMS
from const import CONFIG_TB_ITEMS_DEFAULT
from const import CONFIG_USERS
from const import LOGON
from const import STYLES
from resources.utils import expand_env_vars


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsRestrictions:
    """Dataclass for restrictive settings."""

    allow_all_users: bool
    allow_all_editors: bool
    allow_unsaved: bool
    allow_outside_workspace: bool
    allow_locked_view: bool


@dataclass(slots=True, kw_only=True)
class SettingsTablesTolerancesPositions:
    size: str
    x: int
    y: int


@dataclass(slots=True, kw_only=True)
class SettingsTablesTolerances:
    header_base: str
    header_min: str
    header_max: str
    positions: List[SettingsTablesTolerancesPositions]

    def __post_init__(self) -> None:
        self.positions = [SettingsTablesTolerancesPositions(**i) for i in self.positions]  # type: ignore


@dataclass(slots=True, kw_only=True)
class SettingsTables:
    tolerances: SettingsTablesTolerances

    def __post_init__(self) -> None:
        self.tolerances = SettingsTablesTolerances(**dict(self.tolerances))  # type: ignore


@dataclass(slots=True, kw_only=True)
class SettingsPaths:
    """Dataclass for paths (settings.json)."""

    catia: Path
    release: Path

    def __post_init__(self) -> None:
        self.catia = Path(expand_env_vars(str(self.catia)))
        self.release = Path(expand_env_vars(str(self.release)))


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsFiles:
    """Dataclass for files (settings.json)."""

    app: str
    launcher: str
    workspace: str


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsUrls:
    """Dataclass for urls (settings.json)."""

    help: str | None


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsMails:
    """Dataclass for mails (settings.json)."""

    admin: str


@dataclass(slots=True, kw_only=True)
class Settings:  # pylint: disable=R0902
    """Dataclass for settings (settings.json)."""

    title: str
    debug: bool
    restrictions: SettingsRestrictions
    doc_types: List[str]
    tolerances: List[str]
    tables: SettingsTables
    paths: SettingsPaths
    files: SettingsFiles
    urls: SettingsUrls
    mails: SettingsMails

    def __post_init__(self) -> None:
        self.restrictions = SettingsRestrictions(**dict(self.restrictions))  # type: ignore
        self.tables = SettingsTables(**dict(self.tables))  # type: ignore
        self.files = SettingsFiles(**dict(self.files))  # type: ignore
        self.paths = SettingsPaths(**dict(self.paths))  # type: ignore
        self.urls = SettingsUrls(**dict(self.urls))  # type: ignore
        self.mails = SettingsMails(**dict(self.mails))  # type: ignore


@dataclass(slots=True, kw_only=True, frozen=True)
class Props:
    """Dataclass for properties on the part (properties.json)."""

    partnumber: str
    revision: str
    definition: str

    product: str
    material: str
    base_size: str
    tolerance: str
    creator_3d: str


@dataclass(slots=True, kw_only=True)
class TitleBlockItems:
    """Dataclass for all possible title block items."""

    partnumber: str
    revision: str
    definition: str

    product: str
    material: str
    base_size: str
    tolerance: str

    release_date: str
    document_type: str
    scale: str

    creator_3d: str
    creator_2d: str

    notes: str

    version: str
    path: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the TitleBlockItems dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the TitleBlockItems dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True, frozen=True)
class User:
    """Dataclass for a user (users.json)."""

    logon: str
    id: str
    name: str
    mail: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the User dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the User dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True, frozen=True)
class Info:
    """Dataclass for an info messages (information.json)."""

    counter: int
    msg: str


@dataclass(slots=True, kw_only=True)
class AppData:
    """Dataclass for appdata settings."""

    version: str = field(default=APP_VERSION)
    counter: int = 0
    theme: str = STYLES[0]
    auto_symlink: bool = False

    def __post_init__(self) -> None:
        self.version = (
            APP_VERSION  # Always store the latest version in the appdata json
        )
        self.counter += 1


class Resources:  # pylint: disable=R0902
    """Class for handling resource files."""

    __slots__ = (
        "_settings",
        "_title_block_items",
        "_props",
        "_users",
        "_infos",
        "_appdata",
    )

    def __init__(self) -> None:
        self._read_settings()
        self._read_title_block_items()
        self._read_props()
        self._read_users()
        self._read_infos()
        self._read_appdata()

        atexit.register(self._write_appdata)

    @property
    def settings(self) -> Settings:
        """settings.json"""
        return self._settings

    @property
    def props(self) -> Props:
        """properties.json"""
        return self._props

    @property
    def title_block_items(self) -> TitleBlockItems:
        """title_block_items.json"""
        return self._title_block_items

    @property
    def users(self) -> List[User]:
        """users.json"""
        return self._users

    @property
    def infos(self) -> List[Info]:
        """infos.json"""
        return self._infos

    @property
    def appdata(self) -> AppData:
        """Property for the appdata config file."""
        return self._appdata

    def get_png(self, name: str) -> bytes:
        """Returns a png resource by its name."""
        with importlib.resources.open_binary("resources", name) as f:
            return f.read()

    def _read_settings(self) -> None:
        """Reads the settings json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_SETTINGS) as f:
            self._settings = Settings(**json.load(f))

    def _read_users(self) -> None:
        """Reads the users json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_USERS) as f:
            self._users = [User(**i) for i in json.load(f)]

    def _read_title_block_items(self) -> None:
        """Reads the title block items json from the resources folder."""
        tbi_resource = (
            CONFIG_TB_ITEMS
            if importlib.resources.is_resource("resources", CONFIG_TB_ITEMS)
            else CONFIG_TB_ITEMS_DEFAULT
        )
        with importlib.resources.open_binary("resources", tbi_resource) as f:
            self._title_block_items = TitleBlockItems(**json.load(f))

    def _read_props(self) -> None:
        """Reads the props json from the resources folder."""
        props_resource = (
            CONFIG_PROPS
            if importlib.resources.is_resource("resources", CONFIG_PROPS)
            else CONFIG_PROPS_DEFAULT
        )
        with importlib.resources.open_binary("resources", props_resource) as f:
            self._props = Props(**json.load(f))

    def _read_infos(self) -> None:
        """Reads the information json from the resources folder."""
        infos_resource = (
            CONFIG_INFOS
            if importlib.resources.is_resource("resources", CONFIG_INFOS)
            else CONFIG_INFOS_DEFAULT
        )
        with importlib.resources.open_binary("resources", infos_resource) as f:
            self._infos = [Info(**i) for i in json.load(f)]

    def _read_appdata(self) -> None:
        """Reads the json config file from the appdata folder."""
        if os.path.exists(appdata_file := f"{APPDATA}\\{CONFIG_APPDATA}"):
            with open(appdata_file, "r", encoding="utf8") as f:
                try:
                    value = AppData(**json.load(f))
                except Exception:
                    value = AppData()
                    tkmsg.showwarning(
                        title="Configuration warning",
                        message="The AppData config file has been corrupted. \
                            You may need to apply your preferences again.",
                    )
                self._appdata = value
        else:
            self._appdata = AppData()

    def _write_appdata(self) -> None:
        """Saves appdata config to file."""
        os.makedirs(APPDATA, exist_ok=True)
        with open(f"{APPDATA}\\{CONFIG_APPDATA}", "w", encoding="utf8") as f:
            json.dump(asdict(self._appdata), f)

    def get_user_by_logon(self, logon: Optional[str] = None) -> Optional[User]:
        """
        Returns the user dataclass that matches the logon value. Returns the User of the current
        session if logon is omitted.

        Args:
            logon (Optional[str]): The user to fetch from the dataclass list.

        Returns:
            User: The user from the dataclass list that matches the provided logon name. \
                Returns None if the logon doesn't exist.
        """
        if logon is None:
            logon = LOGON

        for index, value in enumerate(self._users):
            if value.logon == logon:
                return self._users[index]
        return None

    def get_user_by_name(self, name: str) -> Optional[User]:
        """
        Returns the user dataclass that matches the name.

        Args:
            name (str): The username to fetch from the dataclass list.

        Returns:
            User: The user from the dataclass list that matches the provided name.
        """
        for index, value in enumerate(self._users):
            if value.name == name:
                return self._users[index]
        return None

    def logon_exists(self, logon: Optional[str] = None) -> bool:
        """
        Returns wether the users logon exists in the dataclass, or not. Uses the logon-value of the
        current session if logon is omitted.

        Args:
            logon (str): The logon name to search for.

        Returns:
            bool: The user from the dataclass list that matches the provided logon name.
        """
        if logon is None:
            logon = LOGON

        for user in self._users:
            if user.logon == logon:
                return True
        return False

    def get_info_msg_by_counter(self) -> List[str]:
        """
        Returns the info message by the app usage counter.

        Returns:
            List[str]: A list of all messages that should be shown at the counter value.
        """
        values = []
        for index, value in enumerate(self._infos):
            if value.counter == self._appdata.counter:
                values.append(self._infos[index].msg)
        return values


resource = Resources()
