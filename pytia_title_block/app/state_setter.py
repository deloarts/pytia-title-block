"""
    Submodule for managing the state of the widgets.
    The UI is mainly managed by the 'source' of the document.
"""

import tkinter as tk

from pytia.log import log

from app.layout import Layout
from app.vars import Variables


class UISetter:
    """UI Setter class for the main window."""

    def __init__(
        self,
        root: tk.Tk,
        layout: Layout,
        variables: Variables,
    ) -> None:
        """
        Inits the UI Setter class for the main window.

        Args:
            root (tk.Tk): The main window object.
            layout (Layout): The layout of the main window.
            variables (Variables): The variables of the main window.
        """
        self.root = root
        self.layout = layout
        self.vars = variables

    def normal(self) -> None:
        """Sets the UI to state 'normal'."""
        if not self.vars.locked.get():
            log.debug("Setting main UI to state 'normal'.")

            self.layout.input_machine.configure(state=tk.NORMAL)
            self.layout.button_reload_machine.configure(state=tk.NORMAL)

            self.layout.input_partnumber.configure(state=tk.NORMAL)
            self.layout.button_reload_partnumber.configure(state=tk.NORMAL)

            self.layout.input_revision.configure(state=tk.NORMAL)
            self.layout.button_reload_revision.configure(state=tk.NORMAL)

            self.layout.input_definition.configure(state=tk.NORMAL)
            self.layout.button_reload_definition.configure(state=tk.NORMAL)

            self.layout.input_material.configure(state=tk.NORMAL)
            self.layout.button_reload_material.configure(state=tk.NORMAL)

            self.layout.input_base_size.configure(state=tk.NORMAL)
            self.layout.button_reload_base_size.configure(state=tk.NORMAL)

            self.layout.input_tolerance.configure(state=tk.NORMAL)
            self.layout.button_reload_tolerance.configure(state=tk.NORMAL)

            self.layout.input_release_date.configure(state="readonly")

            self.layout.input_doc_type.configure(state="readonly")

            self.layout.button_save.configure(state=tk.NORMAL)

        self.root.config(cursor="arrow")
        self.root.update_idletasks()
        log.info("Main UI state is now 'bought'.")

    def disabled(self) -> None:
        """
        Sets the UI to state 'disabled'.
        """
        log.debug("Setting main UI to state 'disabled'.")

        self.layout.input_machine.configure(state=tk.DISABLED)
        self.layout.button_reload_machine.configure(state=tk.DISABLED)

        self.layout.input_partnumber.configure(state=tk.DISABLED)
        self.layout.button_reload_partnumber.configure(state=tk.DISABLED)

        self.layout.input_revision.configure(state=tk.DISABLED)
        self.layout.button_reload_revision.configure(state=tk.DISABLED)

        self.layout.input_definition.configure(state=tk.DISABLED)
        self.layout.button_reload_definition.configure(state=tk.DISABLED)

        self.layout.input_material.configure(state=tk.DISABLED)
        self.layout.button_reload_material.configure(state=tk.DISABLED)

        self.layout.input_base_size.configure(state=tk.DISABLED)
        self.layout.button_reload_base_size.configure(state=tk.DISABLED)

        self.layout.input_tolerance.configure(state=tk.DISABLED)
        self.layout.button_reload_tolerance.configure(state=tk.DISABLED)

        self.layout.input_release_date.configure(state=tk.DISABLED)

        self.layout.button_save.configure(state=tk.DISABLED)

        self.root.update_idletasks()
