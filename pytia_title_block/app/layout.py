"""
    The layout of the app.
"""
from datetime import datetime
from tkinter import DISABLED
from tkinter import Menu
from tkinter import Tk

from app.frames import Frames
from app.vars import Variables
from const import STYLES
from helper.appearance import set_appearance_menu
from helper.messages import show_help
from resources import resource
from ttkbootstrap import Button
from ttkbootstrap import Checkbutton
from ttkbootstrap import Combobox
from ttkbootstrap import DateEntry
from ttkbootstrap import Entry
from ttkbootstrap import Label
from ttkbootstrap import Menu
from ttkbootstrap import PhotoImage


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

        self._appearance_menu = Menu(menubar, tearoff=False)
        for style in STYLES:
            self._appearance_menu.add_command(label=style)

        self._tools_menu = Menu(menubar, tearoff=False)
        self._tools_menu.add_command(label="Tolerance Table")
        self._tools_menu.add_command(label="Open File Explorer")
        self._tools_menu.add_command(label="Open Linked Document")

        menubar.add_cascade(label="Help", command=show_help)
        menubar.add_cascade(label="Appearance", menu=self._appearance_menu)
        menubar.add_cascade(label="Tools", menu=self._tools_menu)

        set_appearance_menu(self._appearance_menu)
        root.configure(menu=menubar)
        # endregion

        lbl_linked_doc = Label(
            frames.infrastructure,
            text="Linked document",
            width=Layout.LBL_WIDTH,
        )
        lbl_linked_doc.grid(
            row=0,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y, 4),
            sticky="nsew",
        )

        self._lbl_linked_doc = Label(
            frames.infrastructure,
            textvariable=variables.linked_document,
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
        lbl_creator_3d = Label(
            frames.infrastructure,
            text="Creator 3D",
            width=Layout.LBL_WIDTH,
        )
        lbl_creator_3d.grid(
            row=1,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(4, 4),
            sticky="nsew",
        )
        self._lbl_creator_3d = Label(
            frames.infrastructure,
            textvariable=variables.creator_3d,
            width=Layout.LBL_WIDTH,
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
        lbl_creator_2d = Label(
            frames.infrastructure,
            text="Creator 2D",
            width=Layout.LBL_WIDTH,
        )
        lbl_creator_2d.grid(
            row=2,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(4, 4),
            sticky="nsew",
        )
        self._lbl_creator_2d = Label(
            frames.infrastructure,
            textvariable=variables.creator_2d,
            width=Layout.LBL_WIDTH,
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
        lbl_machine = Label(
            frames.infrastructure,
            text="Machine",
            width=Layout.LBL_WIDTH,
        )
        lbl_machine.grid(
            row=4,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y * 2, 2),
            sticky="nsew",
        )

        self._entry_machine = Entry(
            frames.infrastructure,
            textvariable=variables.machine,
            state=DISABLED,
        )
        self._entry_machine.grid(
            row=4,
            column=1,
            padx=(5, 2),
            pady=(Layout.MARGIN_Y * 2, 2),
            sticky="nsew",
        )
        self._btn_reload_machine = Button(
            frames.infrastructure,
            image=self.reload_image,
            style="outline",
            width=3,
            state=DISABLED,
        )
        self._btn_reload_machine.grid(
            row=4,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(Layout.MARGIN_Y * 2, 2),
            sticky="nsew",
        )
        # endregion

        # region PARTNUMBER
        lbl_partnumber = Label(
            frames.infrastructure,
            text="Partnumber",
            width=Layout.LBL_WIDTH,
        )
        lbl_partnumber.grid(
            row=5,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )

        self._entry_partnumber = Entry(
            frames.infrastructure,
            textvariable=variables.partnumber,
            state=DISABLED,
        )
        self._entry_partnumber.grid(
            row=5,
            column=1,
            padx=(5, 2),
            pady=(2, 2),
            sticky="nsew",
        )
        self._btn_reload_partnumber = Button(
            frames.infrastructure,
            image=self.reload_image,
            style="outline",
            width=3,
            state=DISABLED,
        )
        self._btn_reload_partnumber.grid(
            row=5,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(2, 2),
            sticky="nsew",
        )
        # endregion

        # region REVISION
        lbl_revision = Label(
            frames.infrastructure,
            text="Revision",
            width=Layout.LBL_WIDTH,
        )
        lbl_revision.grid(
            row=6,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )

        self._entry_revision = Entry(
            frames.infrastructure,
            textvariable=variables.revision,
            state=DISABLED,
        )
        self._entry_revision.grid(
            row=6,
            column=1,
            padx=(5, 2),
            pady=(2, 2),
            sticky="nsew",
        )
        self._btn_reload_revision = Button(
            frames.infrastructure,
            image=self.reload_image,
            style="outline",
            width=3,
            state=DISABLED,
        )
        self._btn_reload_revision.grid(
            row=6,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(2, 2),
            sticky="nsew",
        )
        # endregion

        # region DEFINITION
        lbl_definition = Label(
            frames.infrastructure,
            text="Definition",
            width=Layout.LBL_WIDTH,
        )
        lbl_definition.grid(
            row=7,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )

        self._entry_definition = Entry(
            frames.infrastructure,
            textvariable=variables.definition,
            state=DISABLED,
        )
        self._entry_definition.grid(
            row=7,
            column=1,
            padx=(5, 2),
            pady=(2, 2),
            sticky="nsew",
        )
        self._btn_reload_definition = Button(
            frames.infrastructure,
            image=self.reload_image,
            style="outline",
            width=3,
            state=DISABLED,
        )
        self._btn_reload_definition.grid(
            row=7,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(2, 2),
            sticky="nsew",
        )
        # endregion

        # region MATERIAL
        lbl_material = Label(
            frames.infrastructure,
            text="Material",
            width=Layout.LBL_WIDTH,
        )
        lbl_material.grid(
            row=8,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y * 2, 2),
            sticky="nsew",
        )

        self._entry_material = Entry(
            frames.infrastructure,
            textvariable=variables.material,
            state=DISABLED,
        )
        self._entry_material.grid(
            row=8,
            column=1,
            padx=(5, 2),
            pady=(Layout.MARGIN_Y * 2, 2),
            sticky="nsew",
        )
        self._btn_reload_material = Button(
            frames.infrastructure,
            image=self.reload_image,
            style="outline",
            width=3,
            state=DISABLED,
        )
        self._btn_reload_material.grid(
            row=8,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(Layout.MARGIN_Y * 2, 2),
            sticky="nsew",
        )
        # endregion

        # region BASE SIZE
        lbl_base_size = Label(
            frames.infrastructure,
            text="Base Size",
            width=Layout.LBL_WIDTH,
        )
        lbl_base_size.grid(
            row=9,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )

        self._entry_base_size = Entry(
            frames.infrastructure,
            textvariable=variables.base_size,
            state=DISABLED,
        )
        self._entry_base_size.grid(
            row=9,
            column=1,
            padx=(5, 2),
            pady=(2, 2),
            sticky="nsew",
        )
        self._btn_reload_base_size = Button(
            frames.infrastructure,
            image=self.reload_image,
            style="outline",
            width=3,
            state=DISABLED,
        )
        self._btn_reload_base_size.grid(
            row=9,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(2, 2),
            sticky="nsew",
        )
        # endregion

        # region TOLERANCE
        lbl_tolerance = Label(
            frames.infrastructure,
            text="Tolerance",
            width=Layout.LBL_WIDTH,
        )
        lbl_tolerance.grid(
            row=10,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )

        self._combo_tolerance = Combobox(
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
            sticky="nsew",
        )
        self._btn_reload_tolerance = Button(
            frames.infrastructure,
            image=self.reload_image,
            style="outline",
            width=3,
            state=DISABLED,
        )
        self._btn_reload_tolerance.grid(
            row=10,
            column=2,
            padx=(2, Layout.MARGIN_X),
            pady=(2, 2),
            sticky="nsew",
        )
        # endregion

        # region DATE
        lbl_date = Label(
            frames.infrastructure,
            text="Release Date",
            width=Layout.LBL_WIDTH,
        )
        lbl_date.grid(
            row=11,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y * 2, 2),
            sticky="nsew",
        )

        self._entry_date = DateEntry(
            master=frames.infrastructure,
            dateformat="%d.%m.%Y",
            startdate=datetime.now(),
            firstweekday=0,
        )
        self._entry_date.entry.configure(
            textvariable=variables.release_date,
            state=DISABLED,
        )
        self._entry_date.button.configure(state=DISABLED)
        self._entry_date.grid(
            row=11,
            column=1,
            padx=(5, 10),
            pady=(Layout.MARGIN_Y * 2, 2),
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region DOC TYPE
        lbl_doc_type = Label(
            frames.infrastructure,
            text="Document type",
            width=Layout.LBL_WIDTH,
        )
        lbl_doc_type.grid(
            row=12,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )
        self._combo_doc_type = Combobox(
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
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region FRAME Footer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self._symlink_toggle = Checkbutton(
            master=frames.footer,
            bootstyle="round-toggle",  # type:ignore
            text="Set Symlink",
            variable=variables.auto_symlink,
            onvalue=True,
            offvalue=False,
        )
        self._symlink_toggle.grid(row=0, column=0, padx=(8, 2), pady=(5, 5), sticky="w")

        self._btn_save = Button(
            frames.footer,
            text="Save",
            style="outline",
            width=10,
            state=DISABLED,
        )
        self._btn_save.grid(row=0, column=1, padx=(5, 2), pady=(5, 5), sticky="e")

        self._btn_abort = Button(
            frames.footer,
            text="Abort",
            style="outline",
            width=10,
        )
        self._btn_abort.grid(row=0, column=2, padx=(2, 10), pady=(5, 5), sticky="e")
        # endregion

    @property
    def tools_menu(self) -> Menu:
        return self._tools_menu

    @property
    def linked_document(self) -> Label:
        return self._lbl_linked_doc

    @property
    def input_machine(self) -> Entry:
        return self._entry_machine

    @property
    def button_reload_machine(self) -> Button:
        return self._btn_reload_machine

    @property
    def input_partnumber(self) -> Entry:
        return self._entry_partnumber

    @property
    def button_reload_partnumber(self) -> Button:
        return self._btn_reload_partnumber

    @property
    def input_revision(self) -> Entry:
        return self._entry_revision

    @property
    def button_reload_revision(self) -> Button:
        return self._btn_reload_revision

    @property
    def input_definition(self) -> Entry:
        return self._entry_definition

    @property
    def button_reload_definition(self) -> Button:
        return self._btn_reload_definition

    @property
    def input_material(self) -> Entry:
        return self._entry_material

    @property
    def button_reload_material(self) -> Button:
        return self._btn_reload_material

    @property
    def input_base_size(self) -> Entry:
        return self._entry_base_size

    @property
    def button_reload_base_size(self) -> Button:
        return self._btn_reload_base_size

    @property
    def input_tolerance(self) -> Combobox:
        return self._combo_tolerance

    @property
    def button_reload_tolerance(self) -> Button:
        return self._btn_reload_tolerance

    @property
    def input_release_date(self) -> DateEntry:
        return self._entry_date

    @property
    def input_doc_type(self) -> Combobox:
        return self._combo_doc_type

    @property
    def toggle_symlink(self) -> Checkbutton:
        return self._symlink_toggle

    @property
    def button_save(self) -> Button:
        return self._btn_save

    @property
    def button_abort(self) -> Button:
        return self._btn_abort
