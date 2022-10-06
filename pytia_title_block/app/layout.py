"""
    The layout of the app.
"""
from datetime import datetime
from tkinter import DISABLED, Menu, PhotoImage, Tk, ttk

from resources import resource
from tkcalendar import DateEntry

from app.frames import Frames
from app.vars import Variables


class Layout:
    """The layout class of the app, holds all widgets."""

    MARGIN_X = 10
    MARGIN_Y = 10
    LBL_WIDTH = 18

    def __init__(self, root: Tk, frames: Frames, variables: Variables) -> None:
        """
        Inits the Layout class. Creates and places the widgets of the main window.

        Args:
            root (Tk): The main window.
            frames (Frames): The frames of the main window.
            variables (Variables): The variables of the main window.
        """
        self.reload_image = PhotoImage(data=resource.get_png("reload.png"))

        # region MENU
        menubar = Menu(root)
        self._tools_menu = Menu(menubar, tearoff=False)
        self._tools_menu.add_command(label="Tolerance Table")

        menubar.add_cascade(label="Tools", menu=self._tools_menu)
        root.configure(menu=menubar)
        # endregion

        lbl_linked_doc = ttk.Label(
            frames.infrastructure,
            text="Linked document",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_linked_doc.grid(
            row=0,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y, 4),
            sticky="nsew",
        )

        self._lbl_linked_doc = ttk.Label(
            frames.infrastructure,
            textvariable=variables.linked_document,
            font=("Segoe UI", 9),
        )
        self._lbl_linked_doc.grid(
            row=0,
            column=1,
            padx=(4, 4),
            pady=(Layout.MARGIN_Y, 2),
            sticky="nsew",
            columnspan=2,
        )

        # region CREATOR 3D
        lbl_creator_3d = ttk.Label(
            frames.infrastructure,
            text="Creator 3D",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_creator_3d.grid(
            row=1,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(4, 4),
            sticky="nsew",
        )
        self._lbl_creator_3d = ttk.Label(
            frames.infrastructure,
            textvariable=variables.creator_3d,
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        self._lbl_creator_3d.grid(
            row=1,
            column=1,
            padx=(5, 10),
            pady=(4, 4),
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region CREATOR 2D
        lbl_creator_2d = ttk.Label(
            frames.infrastructure,
            text="Creator 2D",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_creator_2d.grid(
            row=2,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(4, 4),
            sticky="nsew",
        )
        self._lbl_creator_2d = ttk.Label(
            frames.infrastructure,
            textvariable=variables.creator_2d,
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        self._lbl_creator_2d.grid(
            row=2,
            column=1,
            padx=(5, 10),
            pady=(4, 4),
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region MACHINE
        lbl_machine = ttk.Label(
            frames.infrastructure,
            text="Machine",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_machine.grid(
            row=4,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y * 2, 2),
            sticky="nsew",
        )

        self._entry_machine = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.machine,
            state=DISABLED,
        )
        self._entry_machine.grid(
            row=4,
            column=1,
            padx=(5, 2),
            pady=(Layout.MARGIN_Y * 2, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
        )
        self._btn_reload_machine = ttk.Button(
            frames.infrastructure,
            image=self.reload_image,
            style="Reload.TButton",
            state=DISABLED,
        )
        self._btn_reload_machine.grid(
            row=4,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(Layout.MARGIN_Y * 2 - 1, 1),
            sticky="nsew",
        )
        # endregion

        # region PARTNUMBER
        lbl_partnumber = ttk.Label(
            frames.infrastructure,
            text="Partnumber",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_partnumber.grid(
            row=5,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )

        self._entry_partnumber = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.partnumber,
            state=DISABLED,
        )
        self._entry_partnumber.grid(
            row=5,
            column=1,
            padx=(5, 2),
            pady=(2, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
        )
        self._btn_reload_partnumber = ttk.Button(
            frames.infrastructure,
            image=self.reload_image,
            style="Reload.TButton",
            state=DISABLED,
        )
        self._btn_reload_partnumber.grid(
            row=5,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(1, 1),
            sticky="nsew",
        )
        # endregion

        # region REVISION
        lbl_revision = ttk.Label(
            frames.infrastructure,
            text="Revision",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_revision.grid(
            row=6,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )

        self._entry_revision = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.revision,
            state=DISABLED,
        )
        self._entry_revision.grid(
            row=6,
            column=1,
            padx=(5, 2),
            pady=(2, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
        )
        self._btn_reload_revision = ttk.Button(
            frames.infrastructure,
            image=self.reload_image,
            style="Reload.TButton",
            state=DISABLED,
        )
        self._btn_reload_revision.grid(
            row=6,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(1, 1),
            sticky="nsew",
        )
        # endregion

        # region DEFINITION
        lbl_definition = ttk.Label(
            frames.infrastructure,
            text="Definition",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_definition.grid(
            row=7,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )

        self._entry_definition = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.definition,
            state=DISABLED,
        )
        self._entry_definition.grid(
            row=7,
            column=1,
            padx=(5, 2),
            pady=(2, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
        )
        self._btn_reload_definition = ttk.Button(
            frames.infrastructure,
            image=self.reload_image,
            style="Reload.TButton",
            state=DISABLED,
        )
        self._btn_reload_definition.grid(
            row=7,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(1, 1),
            sticky="nsew",
        )
        # endregion

        # region MATERIAL
        lbl_material = ttk.Label(
            frames.infrastructure,
            text="Material",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_material.grid(
            row=8,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y * 2, 2),
            sticky="nsew",
        )

        self._entry_material = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.material,
            state=DISABLED,
        )
        self._entry_material.grid(
            row=8,
            column=1,
            padx=(5, 2),
            pady=(Layout.MARGIN_Y * 2, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
        )
        self._btn_reload_material = ttk.Button(
            frames.infrastructure,
            image=self.reload_image,
            style="Reload.TButton",
            state=DISABLED,
        )
        self._btn_reload_material.grid(
            row=8,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(Layout.MARGIN_Y * 2 - 1, 1),
            sticky="nsew",
        )
        # endregion

        # region BASE SIZE
        lbl_base_size = ttk.Label(
            frames.infrastructure,
            text="Base Size",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_base_size.grid(
            row=9,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )

        self._entry_base_size = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.base_size,
            state=DISABLED,
        )
        self._entry_base_size.grid(
            row=9,
            column=1,
            padx=(5, 2),
            pady=(2, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
        )
        self._btn_reload_base_size = ttk.Button(
            frames.infrastructure,
            image=self.reload_image,
            style="Reload.TButton",
            state=DISABLED,
        )
        self._btn_reload_base_size.grid(
            row=9,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(1, 1),
            sticky="nsew",
        )
        # endregion

        # region TOLERANCE
        lbl_tolerance = ttk.Label(
            frames.infrastructure,
            text="Tolerance",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_tolerance.grid(
            row=10,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )

        self._combo_tolerance = ttk.Combobox(
            frames.infrastructure,
            values=resource.settings.tolerances,
            textvariable=variables.tolerance,
            state=DISABLED,
        )
        self._combo_tolerance.grid(
            row=10,
            column=1,
            padx=(5, 2),
            pady=(2, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
        )
        self._btn_reload_tolerance = ttk.Button(
            frames.infrastructure,
            image=self.reload_image,
            style="Reload.TButton",
            state=DISABLED,
        )
        self._btn_reload_tolerance.grid(
            row=10,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(1, 1),
            sticky="nsew",
        )
        # endregion

        # region DATE
        lbl_date = ttk.Label(
            frames.infrastructure,
            text="Release Date",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_date.grid(
            row=11,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y * 2, 2),
            sticky="nsew",
        )

        # FIXME: The DateEntry flashes a new window on instantiation.
        self._entry_date = DateEntry(
            master=frames.infrastructure,
            textvariable=variables.release_date,
            date_pattern="dd.mm.yyyy",
            mindate=datetime.now(),
            state=DISABLED,
        )
        self._entry_date.grid(
            row=11,
            column=1,
            padx=(5, 10),
            pady=(Layout.MARGIN_Y * 2, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region DOC TYPE
        lbl_doc_type = ttk.Label(
            frames.infrastructure,
            text="Document type",
            width=Layout.LBL_WIDTH,
            font=("Segoe UI", 9),
        )
        lbl_doc_type.grid(
            row=12,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )
        self._combo_doc_type = ttk.Combobox(
            frames.infrastructure,
            values=resource.settings.doc_types,
            textvariable=variables.document_type,
            state=DISABLED,
        )
        self._combo_doc_type.grid(
            row=12,
            column=1,
            padx=(5, 10),
            pady=(2, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region FRAME Footer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        lbl_info = ttk.Label(
            frames.footer,
            text="",
        )
        lbl_info.grid(
            row=0, column=0, padx=(0, 5), pady=0, ipadx=2, ipady=2, sticky="nsew"
        )

        self._btn_save = ttk.Button(
            frames.footer, text="Save", style="Footer.TButton", state=DISABLED
        )
        self._btn_save.grid(row=0, column=1, padx=(5, 2), pady=(5, 5), sticky="e")

        self._btn_abort = ttk.Button(
            frames.footer, text="Abort", style="Footer.TButton"
        )
        self._btn_abort.grid(row=0, column=2, padx=(2, 10), pady=(5, 5), sticky="e")

    @property
    def tools_menu(self) -> Menu:
        return self._tools_menu

    @property
    def linked_document(self) -> ttk.Label:
        return self._lbl_linked_doc

    @property
    def input_machine(self) -> ttk.Entry:
        return self._entry_machine

    @property
    def button_reload_machine(self) -> ttk.Button:
        return self._btn_reload_machine

    @property
    def input_partnumber(self) -> ttk.Entry:
        return self._entry_partnumber

    @property
    def button_reload_partnumber(self) -> ttk.Button:
        return self._btn_reload_partnumber

    @property
    def input_revision(self) -> ttk.Entry:
        return self._entry_revision

    @property
    def button_reload_revision(self) -> ttk.Button:
        return self._btn_reload_revision

    @property
    def input_definition(self) -> ttk.Entry:
        return self._entry_definition

    @property
    def button_reload_definition(self) -> ttk.Button:
        return self._btn_reload_definition

    @property
    def input_material(self) -> ttk.Entry:
        return self._entry_material

    @property
    def button_reload_material(self) -> ttk.Button:
        return self._btn_reload_material

    @property
    def input_base_size(self) -> ttk.Entry:
        return self._entry_base_size

    @property
    def button_reload_base_size(self) -> ttk.Button:
        return self._btn_reload_base_size

    @property
    def input_tolerance(self) -> ttk.Combobox:
        return self._combo_tolerance

    @property
    def button_reload_tolerance(self) -> ttk.Button:
        return self._btn_reload_tolerance

    @property
    def input_release_date(self) -> ttk.Entry:
        return self._entry_date

    @property
    def input_doc_type(self) -> ttk.Combobox:
        return self._combo_doc_type

    @property
    def button_save(self) -> ttk.Button:
        return self._btn_save

    @property
    def button_abort(self) -> ttk.Button:
        return self._btn_abort
