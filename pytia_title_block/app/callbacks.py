"""
    The callbacks submodule for the main window.
"""

from tkinter import StringVar
from tkinter import Tk
from tkinter import messagebox as tkmsg
from tkinter import ttk

from app.layout import Layout
from app.state_setter import UISetter
from app.vars import Variables
from loader.data_loader import DataLoader
from loader.doc_loader import DocumentLoader
from pytia.log import log
from pytia_ui_tools.widgets.tooltips import ToolTip
from resources import resource
from tools.explorer import explorer
from tools.tolerance_tools import ToleranceTools
from ttkbootstrap import Style


class Callbacks:
    """The callbacks class for the main window."""

    def __init__(
        self,
        root: Tk,
        variables: Variables,
        layout: Layout,
        ui_setter: UISetter,
        doc_loader: DocumentLoader,
        data_loader: DataLoader,
        style: Style,
    ) -> None:
        """
        Initializes the callbacks class.

        Args:
            root (Tk): The main window of the app.
            variables (Variables): The variables of the main window.
            layout (Layout): The layout of the main window.
            ui_setter (UISetter): The ui setter instance of the main window.
            doc_loader (DocumentLoader): The document loader instance.
            data_loader (DataLoader): The data loader instance.
            style (Style): The ttkbootstrap style instance.
        """
        self.root = root
        self.vars = variables
        self.layout = layout
        self.set_ui = ui_setter
        self.doc_loader = doc_loader
        self.data_loader = data_loader
        self.style = style

        self.readonly = bool(
            not resource.logon_exists()
            and not resource.settings.restrictions.allow_all_users
        )

        self._bind_button_callbacks()
        self._bind_widget_callbacks()
        self._bind_menu_callbacks()
        log.info("Callbacks initialized.")

    def _bind_button_callbacks(self) -> None:
        """Binds all callbacks to the main windows buttons."""
        self.layout.button_reload_machine.configure(command=self.on_btn_reload_machine)
        self.layout.button_reload_partnumber.configure(
            command=self.on_btn_reload_partnumber
        )
        self.layout.button_reload_revision.configure(
            command=self.on_btn_reload_revision
        )
        self.layout.button_reload_definition.configure(
            command=self.on_btn_reload_definition
        )
        self.layout.button_reload_material.configure(
            command=self.on_btn_reload_material
        )
        self.layout.button_reload_base_size.configure(
            command=self.on_btn_reload_base_size
        )
        self.layout.button_reload_tolerance.configure(
            command=self.on_btn_reload_tolerance
        )

        self.layout.button_save.configure(command=self.on_btn_save)
        self.layout.button_abort.configure(command=self.on_btn_abort)

    def _bind_widget_callbacks(self) -> None:
        """Binds all callbacks to the main windows widgets."""

    def _bind_menu_callbacks(self) -> None:
        """Binds all callbacks to the menubar."""
        self.layout.tools_menu.entryconfig(0, command=self.on_tools_add_tolerance_table)
        self.layout.tools_menu.entryconfig(1, command=self.on_tools_open_file_explorer)
        self.layout.tools_menu.entryconfig(
            2, command=self.on_tools_open_linked_document
        )

    def _on_btn_reload(
        self,
        variable: StringVar,
        widget: ttk.Entry,
        property_name: str,
    ) -> None:
        """
        Helper method for handling reload buttons.
        Reloads the value from a catia property to a tkinter variable.

        Args:
            variable (StringVar): The tkinter variable that will be reloaded.
            widget (ttk.Entry): The widget to which the variable is linked.
            property_name (str): The name of the catia property, from which to load the data.
        """
        if self.doc_loader.linked_properties is not None:
            value = self.doc_loader.get_property_from_linked_doc(property_name)
            if value is not None:
                variable.set(value)
                widget.configure(foreground=self.style.colors.fg)  # type: ignore
                ToolTip(
                    widget=widget,
                    text="This text has been manually loaded from the linked document.",
                )
            else:
                tkmsg.showinfo(
                    title=resource.settings.title,
                    message=f"Cannot load {str(property_name)!r}: Property not available in linked document.",
                )
        else:
            tkmsg.showinfo(
                title=resource.settings.title,
                message=f"Cannot load {str(property_name)!r}: No linked document available.",
            )

    def on_btn_reload_machine(self) -> None:
        """Callback function for the reload machine button."""
        self._on_btn_reload(
            variable=self.vars.machine,
            widget=self.layout.input_machine,
            property_name=resource.props.machine,
        )

    def on_btn_reload_partnumber(self) -> None:
        """Callback function for the reload partnumber button."""
        self._on_btn_reload(
            variable=self.vars.partnumber,
            widget=self.layout.input_partnumber,
            property_name=resource.props.partnumber,
        )

    def on_btn_reload_revision(self) -> None:
        """Callback function for the reload revision button."""
        self._on_btn_reload(
            variable=self.vars.revision,
            widget=self.layout.input_revision,
            property_name=resource.props.revision,
        )

    def on_btn_reload_definition(self) -> None:
        """Callback function for the reload definition button."""
        self._on_btn_reload(
            variable=self.vars.definition,
            widget=self.layout.input_definition,
            property_name=resource.props.definition,
        )

    def on_btn_reload_material(self) -> None:
        """Callback function for the reload material button."""
        self._on_btn_reload(
            variable=self.vars.material,
            widget=self.layout.input_material,
            property_name=resource.props.material,
        )

    def on_btn_reload_base_size(self) -> None:
        """Callback function for the reload base size button."""
        self._on_btn_reload(
            variable=self.vars.base_size,
            widget=self.layout.input_base_size,
            property_name=resource.props.base_size,
        )

    def on_btn_reload_tolerance(self) -> None:
        """Callback function for the reload tolerance button."""
        self._on_btn_reload(
            variable=self.vars.tolerance,
            widget=self.layout.input_tolerance,
            property_name=resource.props.tolerance,
        )

    def on_tools_add_tolerance_table(self) -> None:
        """Creates a new tolerance table (based on all ALP tolerances of all views)"""
        tol_tools = ToleranceTools(doc_loader=self.doc_loader)
        tol_tools.add_table()

    def on_tools_open_linked_document(self) -> None:
        """Opens the linked document and closes the app."""
        self.doc_loader.open_linked()

    def on_tools_open_file_explorer(self) -> None:
        """Opens the file explorer."""
        explorer(self.doc_loader.path)

    def on_btn_save(self) -> None:
        """
        Event handler for the OK button. Verifies the user input and saves the changes to the
        documents properties.
        """
        log.info("Callback for button 'Save'.")
        self.data_loader.load_into_title_block()
        self.doc_loader.save_drawing_path_to_linked_document()

        self.root.withdraw()
        self.root.destroy()

    def on_btn_abort(self) -> None:
        """Callback function for the abort button. Closes the app."""
        log.info("Callback for button 'Abort'.")
        self.root.withdraw()
        self.root.destroy()
