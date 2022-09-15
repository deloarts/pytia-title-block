"""
    Document loader for the UI.
"""

import atexit
import os
from pathlib import Path
from tkinter import messagebox as tkmsg

from const import PROP_DRAWING_PATH
from pytia.exceptions import PytiaDocumentNotSavedError
from pytia.framework import framework
from pytia.framework.drafting_interfaces.drawing_text import DrawingText
from pytia.framework.drafting_interfaces.drawing_view import DrawingView
from pytia.framework.product_structure_interfaces.product import Product
from pytia.log import log
from pytia.wrapper.documents.drawing_documents import PyDrawingDocument
from pytia.wrapper.properties import PyProperties
from resources import resource


class DocumentLoader:
    """Helper class to handle document operations."""

    def __init__(self) -> None:
        """Initialize the document loader."""
        self.active_document = framework.catia.active_document

        self._lock_catia(True)
        atexit.register(lambda: self._lock_catia(False))

        if not resource.settings.restrictions.allow_unsaved and not os.path.isabs(
            self.active_document.full_name
        ):
            raise PytiaDocumentNotSavedError(
                "It is not allowed to edit the parameters of an unsaved document. "
                "Please save the document first."
            )

        self.drawing_document = PyDrawingDocument()
        self.drawing_document.current()
        self.name = self.drawing_document.document.name

        self.sheets = self.drawing_document.drawing_document.sheets
        self.sheet = self.sheets.active_sheet
        self.views = self.sheet.views
        self.foreground_view = self.views.item(1)
        self.background_view = self.views.item(2)

        self.fg_texts = self.foreground_view.texts
        self.bg_texts = self.background_view.texts

        self._linked_view = None
        self._linked_product = None
        self._linked_properties = None
        self.get_linked()

    @property
    def path(self) -> Path:
        """Returns the documents absolute path with filename and file extension."""
        return Path(self.drawing_document.document.full_name)

    @property
    def folder(self) -> Path:
        """Returns the folder as absolute path in which this document is saved."""
        return Path(self.path).parent

    @property
    def linked_view(self) -> DrawingView | None:
        """Returns the first view of the linked document."""
        return self._linked_view

    @property
    def linked_product(self) -> Product | None:
        """Returns the product object of the linked document."""
        return self._linked_product

    @property
    def linked_properties(self) -> PyProperties | None:
        """Returns the properties of the linked document."""
        return self._linked_properties

    def _lock_catia(self, value: bool) -> None:
        """
        Sets the lock-state of catia.

        Args:
            value (bool): True: Locks the catia UI, False: Releases the lock.
        """
        log.debug(f"Setting catia lock to {value!r}")
        framework.catia.refresh_display = not value
        framework.catia.interactive = not value
        framework.catia.display_file_alerts = value
        framework.catia.undo_redo_lock = value
        if value:
            framework.catia.disable_new_undo_redo_transaction()
        else:
            framework.catia.enable_new_undo_redo_transaction()

    def get_linked(self) -> None:
        """Retrieve the linked view, doc and properties from the first view."""
        if self.views.count > 2:
            first_view = self.views.item(3)
            if first_view.is_generative():
                com_doc = first_view.generative_behavior.document.com_object
                self._linked_view = first_view
                self._linked_product = Product(com_doc)
                self._linked_properties = PyProperties(self._linked_product)
                self.save_drawing_path_to_linked_document()
                log.info(f"Linked document {self._linked_product.full_name!r}.")
            else:
                log.info(
                    f"Cannot link view {first_view.name!r}: View is not generative."
                )
        else:
            log.info("No document available to link.")

    def get_text_by_name(self, name: str) -> DrawingText | None:
        """
        Returns the drawing text item of the document, which component name matches the given name.
        Searches for the name in all views.

        Args:
            name (str): The name of the drawing text item.

        Returns:
            DrawingText | None: The item or None, if the given name does not exist as drawing text.
        """
        for view_index in range(1, self.views.count + 1):
            for _ in range(1, self.views.item(view_index).texts.count + 1):
                try:
                    text = DrawingText(
                        self.views.item(view_index).texts.get_item(name).com_object
                    )
                    log.info(
                        f"Retrieved text element {name!r} from view {view_index!r}."
                    )
                    return text
                except:
                    pass
        log.warning(f"No text element {name!r} found in drawing document.")
        return None

    def get_text_value_by_name(self, name: str) -> str | None:
        """
        Returns the drawing text's value by its name.

        Args:
            name (str): The name of the drawing text, from which the value is retrieved.

        Returns:
            str | None: The value or None, if the given name does not exist as drawing text.
        """
        text = self.get_text_by_name(name)
        return text.text if text is not None and text.text != "-" else None

    def set_text_value(self, value: str, name: str) -> None:
        """
        Sets the drawing text's value to the given value.

        Args:
            value (str): The value to set.
            name (str): The component name of the drawing text.
        """
        text = self.get_text_by_name(name)
        if value == "":
            value = "-"

        if text is not None:
            text.text = value
            log.info(f"Wrote value {value!r} to text element {name!r}.")

    def get_property_from_linked_doc(self, name: str | None) -> str | None:
        """
        Returns a properties' value from the linked document. Returns None if one of the 
        following conditions are met:
         - No linked document available
         - No properties available
         - The property does not exist

        Args:
            name (str): The name of the property. Returns the CATIA standard properties when the \
                name is `partnumber`, `definition`, `revision`, `nomenclature`, `source`, or \
                `description`.

        Returns:
            str | None: The value of the property. Returns None if the property does not exist.
        """
        if name is None:
            return None

        if self.linked_product is not None and self.linked_properties is not None:
            if name == "partnumber":
                return self.linked_product.part_number
            elif name == "definition":
                return self.linked_product.definition
            elif name == "revision":
                return self.linked_product.revision
            elif name == "nomenclature":
                return self.linked_product.nomenclature
            elif name == "source":
                return str(self.linked_product.source)
            elif name == "description":
                return self.linked_product.description_reference
            elif self.linked_properties.exists(name):
                return self.linked_properties.get_by_name(name).value
        log.warning(f"No property {name!r} found in linked document.")
        return None

    def save_drawing_path_to_linked_document(self) -> None:
        """Writes the drawing path to the linked document."""
        if self.linked_properties is None:
            log.warning("No linked document, skipping saving drawing path.")
            return

        if self.linked_properties.exists(PROP_DRAWING_PATH):
            existing_path = str(
                Path(self.linked_properties.get_by_name(PROP_DRAWING_PATH).value)
            )
            if existing_path != str(self.path):
                if not tkmsg.askyesno(
                    title=resource.settings.title,
                    message=(
                        "A drawing file already exists for the linked document at "
                        f"{existing_path!r}.\n\n"
                        "Do you want to overwrite the drawing file path in the linked document "
                        "with the path of the current drawing?"
                    ),
                ):
                    return
            self.linked_properties.delete(PROP_DRAWING_PATH)

        if self.path.is_absolute():
            self.linked_properties.create(
                name=PROP_DRAWING_PATH,
                value=str(self.path),
            )
            log.info(f"Wrote drawing path {str(self.path)!r} to linked document.")
        else:
            tkmsg.showwarning(
                title=resource.settings.title,
                message=(
                    "Could not save the drawing path to the linked document: "
                    "The current drawing document is not saved. Please save the document first."
                ),
            )
