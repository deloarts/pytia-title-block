"""
    The main window for the application.
"""

import tkinter as tk
from pathlib import Path
from tkinter import font
from tkinter import messagebox as tkmsg

import ttkbootstrap as ttk
from app.callbacks import Callbacks
from app.frames import Frames
from app.layout import Layout
from app.state_setter import UISetter
from app.tooltips import ToolTips
from app.traces import Traces
from app.vars import Variables
from const import APP_VERSION
from const import LOG
from const import LOGON
from const import LOGS
from helper.messages import show_help
from loader.data_loader import DataLoader
from loader.doc_loader import DocumentLoader
from pytia.exceptions import PytiaBodyEmptyError
from pytia.exceptions import PytiaDifferentDocumentError
from pytia.exceptions import PytiaDocumentNotSavedError
from pytia.exceptions import PytiaNoDocumentOpenError
from pytia.exceptions import PytiaPropertyNotFoundError
from pytia.exceptions import PytiaWrongDocumentTypeError
from pytia_ui_tools.exceptions import PytiaUiToolsOutsideWorkspaceError
from pytia_ui_tools.handlers.error_handler import ErrorHandler
from pytia_ui_tools.handlers.mail_handler import MailHandler
from pytia_ui_tools.handlers.workspace_handler import Workspace
from pytia_ui_tools.window_manager import WindowManager
from resources import resource


class GUI(tk.Tk):
    """The user interface of the app."""

    WIDTH = 450
    HEIGHT = 520

    def __init__(self) -> None:
        """Inits the main window."""
        ttk.tk.Tk.__init__(self)
        self.style = ttk.Style(theme=resource.appdata.theme)

        # CLASS VARS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.doc_loader: DocumentLoader  # Instantiate later for performance improvement
        self.data_loader: DataLoader  # Instantiate later for
        self.workspace: Workspace  # Instantiate later, dependent on doc_helper
        self.set_ui: UISetter  # Instantiate later, dependent on doc_helper
        self.vars = Variables(root=self)
        self.frames = Frames(root=self)
        self.layout = Layout(
            root=self,
            frames=self.frames,
            variables=self.vars,
        )

        self.readonly = bool(
            not resource.logon_exists()
            and not resource.settings.restrictions.allow_all_users
        )

        # UI TOOLS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.window_manager = WindowManager(self)
        self.mail_handler = MailHandler(
            standard_receiver=resource.settings.mails.admin,
            app_title=resource.settings.title,
            app_version=APP_VERSION,
            logfile=Path(LOGS, LOG),
        )
        self.error_handler = ErrorHandler(
            mail_handler=self.mail_handler,
            warning_exceptions=[
                PytiaNoDocumentOpenError,
                PytiaWrongDocumentTypeError,
                PytiaBodyEmptyError,
                PytiaPropertyNotFoundError,
                PytiaDifferentDocumentError,
                PytiaDocumentNotSavedError,
                PytiaUiToolsOutsideWorkspaceError,
            ],
        )

        # UI INIT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.title(
            f"{resource.settings.title} "
            f"{'(DEBUG MODE)' if resource.settings.debug else APP_VERSION}"
            f"{' (READ ONLY)' if self.readonly else ''}"
        )
        self.attributes("-topmost", True)
        self.attributes("-toolwindow", True)
        self.config(cursor="wait")
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=9)
        self.report_callback_exception = self.error_handler.exceptions_callback

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (GUI.WIDTH / 2))
        y_coordinate = int((screen_height / 2) - (GUI.HEIGHT / 2) - 20)
        self.geometry(f"{GUI.WIDTH}x{GUI.HEIGHT}+{x_coordinate}+{y_coordinate}")
        self.minsize(width=GUI.WIDTH, height=GUI.HEIGHT)

        self.update()
        self.window_manager.remove_window_buttons()

    def run(self) -> None:
        """Run the app."""
        self.after(100, self.run_controller)
        self.mainloop()

    def run_controller(self) -> None:
        """Runs all controllers. Initializes all lazy loaders, bindings and traces."""
        self.doc_loader = DocumentLoader(variables=self.vars)
        self.data_loader = DataLoader(
            variables=self.vars, doc_loader=self.doc_loader, layout=self.layout
        )
        self.workspace = Workspace(
            path=self.doc_loader.path,
            filename=resource.settings.files.workspace,
            allow_outside_workspace=resource.settings.restrictions.allow_outside_workspace,
        )
        self.workspace.read_yaml()
        self.doc_loader.set_workspace(self.workspace)

        if ws_title := self.workspace.elements.title:
            self.title(f"{self.title()}  -  {ws_title} (Workspace)")

        self.set_ui = UISetter(
            root=self,
            layout=self.layout,
            variables=self.vars,
        )
        self.callbacks()
        self.traces()
        self.bindings()
        self.main_controller()

    def main_controller(self) -> None:
        """
        The main controller.
        - Retrieves the properties from the document (part or product).
        - Loads all tooltips (some of them depend on some properties).
        - Sets the UI state based on the restrictions of the settings.json and the workspace file.
        """
        self.set_ui.disabled()
        self.tooltips()

        if not self.workspace.elements.active:
            self.set_ui.disabled()
            tkmsg.showinfo(
                message=(
                    "This workspace is disabled. You cannot make changes to this document."
                )
            )
            return

        if self.readonly:
            self.set_ui.disabled()
            tkmsg.showinfo(
                message=(
                    f"You are not allowed to make changes to the part properties: {LOGON} is not "
                    f"available in the user configuration."
                )
            )
            return

        if (
            self.workspace.elements.editors
            and LOGON not in self.workspace.elements.editors
            and not resource.settings.restrictions.allow_all_editors
        ):
            self.set_ui.disabled()
            tkmsg.showinfo(
                message=(
                    f"You are not allowed to make changes to the part properties: {LOGON} is not "
                    f"available in the workspace configuration."
                )
            )
            return

        self.data_loader.load_into_app()
        self.set_ui.normal()

    def bindings(self) -> None:
        """Key bindings."""
        self.bind("<Escape>", lambda _: self.destroy())
        self.bind("<F1>", lambda _: show_help())
        self.bind("<F5>", lambda _: self.main_controller())
        # FIXME: There is a bug on the middle mouse button, where, when the button is clicked,
        # selected text will be inserted into a widget, when the cursor hovers above the widget.
        # I can't find the source of the bug, this is a to do.
        # self.bind("<Button-2>", lambda _: self.on_btn_save())

    def callbacks(self) -> None:
        """Instantiates the Callbacks class."""
        Callbacks(
            root=self,
            variables=self.vars,
            layout=self.layout,
            ui_setter=self.set_ui,
            doc_loader=self.doc_loader,
            data_loader=self.data_loader,
            style=self.style,
        )

    def traces(self) -> None:
        """Instantiates the traces class."""
        Traces(
            variables=self.vars,
            state_setter=self.set_ui,
        )

    def tooltips(self) -> None:
        """Instantiates the tooltips class."""
        ToolTips(layout=self.layout)
