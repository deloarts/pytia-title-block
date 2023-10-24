"""
    Frames submodule for the main window.
"""

from tkinter import Tk

from ttkbootstrap import Frame
from ttkbootstrap import Labelframe


class Frames:
    """Frames class for the main window. Holds all ttk frames."""

    def __init__(self, root: Tk) -> None:
        self._frame_infra = Frame(
            master=root,
        )
        self._frame_infra.grid(
            row=0, column=0, sticky="nsew", padx=(5, 10), pady=(10, 10)
        )
        self._frame_infra.grid_columnconfigure(1, weight=1)
        self._frame_infra.grid_rowconfigure(14, weight=1)

        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self._frame_footer = Frame(master=root, height=30)
        self._frame_footer.grid(
            row=1, column=0, sticky="swe", padx=10, pady=(5, 10), columnspan=1
        )
        self._frame_footer.grid_columnconfigure(1, weight=1)

    @property
    def infrastructure(self) -> Frame:
        """Returns the infrastructure frame."""
        return self._frame_infra

    @property
    def footer(self) -> Frame:
        """Returns the footer frame."""
        return self._frame_footer
