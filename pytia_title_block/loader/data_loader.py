"""
    Data loader submodule.
"""

from datetime import datetime
from fractions import Fraction
from tkinter import StringVar, ttk

from app.layout import Layout
from app.vars import Variables
from const import APP_NAME, APP_VERSION, LOGON
from pytia_ui_tools.widgets.tooltips import ToolTip
from resources import resource

from loader.doc_loader import DocumentLoader


class DataLoader:
    """Class for loading data from and to the app."""

    def __init__(
        self, variables: Variables, layout: Layout, doc_loader: DocumentLoader
    ) -> None:
        """
        Inits the class.

        Args:
            variables (Variables): The variables of the application.
            layout (Layout): The layout of the application.
            doc_loader (DocumentLoader): The document loader instance.
        """
        self.doc_loader = doc_loader
        self.vars = variables
        self.layout = layout

    def _set_var(
        self,
        variable: StringVar,
        widget: ttk.Entry | ttk.Combobox,
        title_block_item: str,
        property_name: str | None = None,
        default_value: str | None = None,
    ) -> None:
        """
        Sets a tkinter variable.
        The variable's value will be either set from the title block, the linked document or
        the default value (in this order, in case multiple sources have values.)

        Args:
            variable (StringVar): The tkinter variable to set.
            widget (ttk.Entry | ttk.Combobox): The widget to which the variable belongs. \
                This is used for tooltips and visual changes.
            title_block_item (str): The component name of the title block item, from which to \
                fetch data.
            property_name (str | None, optional): The property name from which to fetch data. \
                This is optional, if no name is given, the data will be fetched from the title \
                    block alone (or the default value). Defaults to None.
            default_value (str | None, optional): The default value. Will be used if all other \
                sources are None. Defaults to None.
        """
        text_value = self.doc_loader.get_text_value_by_name(title_block_item)
        prop_value = self.doc_loader.get_property_from_linked_doc(property_name)

        variable.set(text_value or prop_value or default_value or "")

        if (
            text_value is not None
            and property_name is not None
            and text_value != prop_value
        ):
            widget.configure(foreground="red")
            ToolTip(
                widget=widget,
                text=(
                    "This text has been loaded from the title block.\n\n"
                    "The text is red, because the values between the title block and the "
                    "linked document are not the same:\n\n"
                    f"  Title block: {text_value}\n"
                    f"  Linked document: {prop_value}\n\n"
                    "If you want to use the text value from the linked document, use the "
                    "reload button at the side."
                ),
            )
        elif text_value is not None and text_value != "":
            ToolTip(
                widget=widget,
                text="This text has been loaded from the title block.",
            )
        elif prop_value is not None and prop_value != "":
            ToolTip(
                widget=widget,
                text="This text has been loaded from the linked document.",
            )
        elif default_value is not None and default_value != "":
            ToolTip(
                widget=widget,
                text="This text is the default value for this field.",
            )

    def _set_var_username(self, variable: StringVar, logon: str | None) -> None:
        """
        Translates the given logon to the user's name and sets it to the given variable.

        Args:
            variable (StringVar): The tkinter variable, which holds the user's name.
            logon (str | None): The logon to translate.
        """
        user = resource.get_user_by_logon(logon)
        variable.set(user.name if user else f"Unknown user ({logon})")

    def _get_scale(self) -> str:
        """Returns the first view's scale as fraction (1:1, 1:5, ...)."""
        if not self.doc_loader.linked_view:
            return "-"
        f_scale = Fraction(self.doc_loader.linked_view.scale)
        return f"{f_scale.numerator}:{f_scale.denominator}"

    def load_into_app(self) -> None:
        """Loads all data into the app."""
        if self.doc_loader.linked_product is None:
            self.vars.linked_document.set("No document linked.")
        else:
            self.vars.linked_document.set(
                f"{self.doc_loader.linked_product.part_number}"
                f" Rev{self.doc_loader.linked_product.revision}"
            )

        self._set_var(
            variable=self.vars.machine,
            widget=self.layout.input_machine,
            title_block_item=resource.title_block_items.machine,
            property_name=resource.props.machine,
        )

        self._set_var(
            variable=self.vars.partnumber,
            widget=self.layout.input_partnumber,
            title_block_item=resource.title_block_items.partnumber,
            property_name=resource.props.partnumber,
        )

        self._set_var(
            variable=self.vars.revision,
            widget=self.layout.input_revision,
            title_block_item=resource.title_block_items.revision,
            property_name=resource.props.revision,
        )

        self._set_var(
            variable=self.vars.definition,
            widget=self.layout.input_definition,
            title_block_item=resource.title_block_items.definition,
            property_name=resource.props.definition,
        )

        self._set_var(
            variable=self.vars.material,
            widget=self.layout.input_material,
            title_block_item=resource.title_block_items.material,
            property_name=resource.props.material,
        )

        self._set_var(
            variable=self.vars.base_size,
            widget=self.layout.input_base_size,
            title_block_item=resource.title_block_items.base_size,
            property_name=resource.props.base_size,
        )

        self._set_var(
            variable=self.vars.tolerance,
            widget=self.layout.input_tolerance,
            title_block_item=resource.title_block_items.tolerance,
            property_name=resource.props.tolerance,
        )

        self._set_var(
            variable=self.vars.release_date,
            widget=self.layout.input_release_date,
            title_block_item=resource.title_block_items.release_date,
            default_value=datetime.now().strftime("%d.%m.%Y"),
        )

        self._set_var(
            variable=self.vars.document_type,
            widget=self.layout.input_doc_type,
            title_block_item=resource.title_block_items.document_type,
            default_value=resource.settings.doc_types[0],
        )

        self._set_var_username(
            variable=self.vars.creator_3d,
            logon=self.doc_loader.get_property_from_linked_doc(
                resource.props.creator_3d
            ),
        )

        self._set_var_username(
            variable=self.vars.creator_2d,
            logon=LOGON,
        )

    def load_into_title_block(self) -> None:
        """Loads (writes) all data into the title block."""
        self.doc_loader.set_text_value(
            value=self.vars.machine.get(), name=resource.title_block_items.machine
        )
        self.doc_loader.set_text_value(
            value=self.vars.partnumber.get(), name=resource.title_block_items.partnumber
        )
        self.doc_loader.set_text_value(
            value=self.vars.revision.get(), name=resource.title_block_items.revision
        )
        self.doc_loader.set_text_value(
            value=self.vars.definition.get(), name=resource.title_block_items.definition
        )

        self.doc_loader.set_text_value(
            value=self.vars.material.get(), name=resource.title_block_items.material
        )
        self.doc_loader.set_text_value(
            value=self.vars.base_size.get(), name=resource.title_block_items.base_size
        )
        self.doc_loader.set_text_value(
            value=self.vars.tolerance.get(), name=resource.title_block_items.tolerance
        )

        self.doc_loader.set_text_value(
            value=self.vars.release_date.get(),
            name=resource.title_block_items.release_date,
        )
        self.doc_loader.set_text_value(
            value=self.vars.document_type.get(),
            name=resource.title_block_items.document_type,
        )

        self.doc_loader.set_text_value(
            value=self.vars.creator_3d.get(), name=resource.title_block_items.creator_3d
        )
        self.doc_loader.set_text_value(
            value=self.vars.creator_2d.get(), name=resource.title_block_items.creator_2d
        )

        self.doc_loader.set_text_value(
            value=self._get_scale(), name=resource.title_block_items.scale
        )
        self.doc_loader.set_text_value(
            value=f"{APP_NAME} v{APP_VERSION}", name=resource.title_block_items.version
        )
        self.doc_loader.set_text_value(
            value=str(self.doc_loader.path), name=resource.title_block_items.path
        )
