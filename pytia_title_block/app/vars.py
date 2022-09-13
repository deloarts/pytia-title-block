"""
    The variables submodule for the app.
"""

from dataclasses import dataclass
from tkinter import StringVar, Tk


@dataclass(slots=True, kw_only=True)
class Variables:
    """Dataclass for the main windows variables."""

    linked_document: StringVar

    creator_3d: StringVar
    creator_2d: StringVar

    machine: StringVar
    partnumber: StringVar
    revision: StringVar
    definition: StringVar

    material: StringVar
    base_size: StringVar
    tolerance: StringVar

    release_date: StringVar
    document_type: StringVar

    def __init__(self, root: Tk) -> None:
        """
        Inits the variables.

        Args:
            root (Tk): The main window.
        """

        self.linked_document = StringVar(master=root, name="linked_document", value="-")

        self.creator_3d = StringVar(master=root, name="creator_3d", value="-")
        self.creator_2d = StringVar(master=root, name="creator_2d", value="-")

        self.machine = StringVar(master=root, name="machine")
        self.partnumber = StringVar(master=root, name="partnumber")
        self.revision = StringVar(master=root, name="revision")
        self.definition = StringVar(master=root, name="definition")

        self.material = StringVar(master=root, name="material")
        self.base_size = StringVar(master=root, name="base_size")
        self.tolerance = StringVar(master=root, name="tolerance")

        self.release_date = StringVar(master=root, name="release_date")
        self.document_type = StringVar(master=root, name="document_type")
