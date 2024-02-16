"""
    Document loader for the UI.
"""

import os
import sys
from pathlib import Path
from tkinter import messagebox as tkmsg
from typing import List

from app.vars import Variables
from const import PROP_DRAWING_PATH
from pycatia.drafting_interfaces.drawing_text import DrawingText
from pycatia.drafting_interfaces.drawing_view import DrawingView
from pycatia.in_interfaces.document import Document
from pycatia.product_structure_interfaces.product import Product
from pytia.exceptions import PytiaDocumentNotSavedError
from pytia.framework import framework
from pytia.log import log
from pytia.wrapper.documents.drawing_documents import PyDrawingDocument
from pytia.wrapper.properties import PyProperties
from pytia_ui_tools.handlers.workspace_handler import Workspace
from resources import resource
from resources.utils import create_path_symlink
from resources.utils import create_path_workspace_level


class DocumentLoader:
    """Helper class to handle document operations."""

    def __init__(self, variables: Variables) -> None:
        """Initialize the document loader."""
        self.vars = variables
        self.workspace: Workspace | None = None
        self.active_document = framework.catia.active_document

        # FIXME: Locking CATIA prevents the ability to detect changes on the document.
        # This means that the part or product won't be saved, even if the user tries to manually
        # save it.
        # self._lock_catia(True)
        # atexit.register(lambda: self._lock_catia(False))

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

        self._linked_doc = None
        self._linked_view = None
        self._linked_product = None
        self._linked_properties = None

        self.check_title_block()
        self.get_linked()

    @property
    def path(self) -> Path:
        """Returns the documents absolute path with filename and file extension."""
        return Path(self.drawing_document.document.full_name).resolve()

    @property
    def folder(self) -> Path:
        """Returns the folder as absolute path in which this document is saved."""
        return Path(self.path).parent

    @property
    def linked_document(self) -> Document | None:
        """Returns the document object of the linked document."""
        return self._linked_doc

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

    def set_workspace(self, workspace: Workspace) -> None:
        """Takes the workspace object and stores it in the class"""
        self.workspace = workspace

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

    def get_all_open_documents(self) -> List[str]:
        """Returns a list of all open documents (document.name)"""
        open_documents: List[str] = []
        for i in range(1, framework.catia.documents.count + 1):
            open_documents.append(framework.catia.documents.item(i).name)
        return open_documents

    def get_all_open_windows(self) -> List[str]:
        """Returns a list of all open windows"""
        open_windows: List[str] = []
        for i in range(1, framework.catia.windows.count + 1):
            open_windows.append(framework.catia.windows.item(i).name)
        return open_windows

    def check_title_block(self) -> None:
        for item in resource.title_block_items.values:
            missing_items = []
            if self.get_text_by_name(item) is None:
                missing_items.append(item)
            if missing_items:
                tkmsg.showwarning(
                    title=resource.settings.title,
                    message=(
                        "The title block of the current document doesn't have all required items. "
                        "It is possible, that some information will be lost. Please consider "
                        "updating the title block.\n\nItems missing:\n"
                        f"{', '.join(missing_items)}"
                    ),
                )
                return

    def get_linked(self) -> None:
        """Retrieve the linked view, doc and properties from the first view."""
        if self.views.count > 2:
            first_view = self.views.item(3)
            if (
                first_view.lock_status
                and not resource.settings.restrictions.allow_locked_view
            ):
                self.vars.locked.set(True)
                tkmsg.showinfo(
                    title=resource.settings.title,
                    message=(
                        "The settings are set to disable this app if the first view is locked. "
                        "Unlock the first view to enable editing.\n\n"
                        "But take into account, there is a reason why the view is locked."
                    ),
                )

            if first_view.is_generative():
                self._linked_view = first_view
                com_doc = first_view.generative_behavior.document.com_object

                self._linked_product = Product(com_doc)
                self._linked_doc = Document(self._linked_product.parent.com_object)
                self._linked_properties = PyProperties(self._linked_product)
                log.info(f"Linked document {self._linked_product.full_name!r}.")
            else:
                log.info(
                    f"Cannot link view {first_view.name!r}: View is not generative."
                )
        else:
            log.info("No document available to link.")

    def open_linked(self) -> None:
        """Opens the linked document and closes the app."""
        if self.linked_document:
            if self.linked_document.name in self.get_all_open_windows():
                framework.catia.windows.item(self.linked_document.name).activate()
                log.info(f"User opened linked document (window).")
                sys.exit()
            if self.linked_document.path().is_file():
                framework.catia.documents.open(str(self.linked_document.path()))
                log.info(f"User opened linked document (file).")
                sys.exit()
        tkmsg.showinfo(
            title=resource.settings.title, message="No linked document found."
        )

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
        document_path = self._get_linked_document_save_path()

        if document_path is None:
            return

        if self.linked_document and self.linked_properties:
            linked_drawing_path = self.linked_properties.get_by_name(
                PROP_DRAWING_PATH
            ).value

            if not self.linked_properties.exists(PROP_DRAWING_PATH):
                self._save_path_to_linked_document(document_path)
                return

            if linked_drawing_path != document_path and tkmsg.askyesno(
                title=resource.settings.title,
                message=(
                    "A drawing file already exists for the linked document at "
                    f"{linked_drawing_path!r}.\n\n"
                    "Do you want to overwrite the drawing file path in the linked document "
                    "with the path of the current drawing?\n\n"
                    f"The current drawing path is: {str(document_path)!r}"
                ),
            ):
                self._save_path_to_linked_document(document_path)
                return

    def _get_linked_document_save_path(self) -> str | None:
        if self.path.is_absolute():
            if self.workspace and self.workspace.workspace_folder:
                return create_path_workspace_level(
                    path=self.path,
                    workspace_folder=self.workspace.workspace_folder,
                    always_apply_relative=resource.appdata.auto_symlink,
                )
            else:
                return create_path_symlink(
                    path=self.path,
                    alway_apply_symlink=resource.appdata.auto_symlink,
                )
        else:
            tkmsg.showwarning(
                title=resource.settings.title,
                message=(
                    "Could not get the filepath from this document: "
                    "The current drawing document is not saved. Please save the document first."
                ),
            )

    def _save_path_to_linked_document(self, drawing_path: str) -> None:
        if self.linked_document and self.linked_properties:
            if self.linked_properties.exists(PROP_DRAWING_PATH):
                self.linked_properties.delete(PROP_DRAWING_PATH)

            self.linked_properties.create(
                name=PROP_DRAWING_PATH,
                value=drawing_path,
            )

            # FIXME: This loads the linked document as active document, but only if the linked
            #        document is already open. If the linked document isn't open, this works
            #        perfectly fine.
            #        Temporary fix: Close the linked document.
            self.linked_document.save()
            self.linked_document.close()

            log.info(
                f"Wrote drawing path {drawing_path!r} to linked document {self.linked_document.name!r}."
            )
        else:
            tkmsg.showwarning(
                title=resource.settings.title,
                message=(
                    "Could not save the drawing path to the linked document: "
                    "No linked document found."
                ),
            )
