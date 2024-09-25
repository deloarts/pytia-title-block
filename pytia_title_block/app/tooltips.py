"""
    Tooltips submodule for the app.
"""

from app.layout import Layout
from pytia_ui_tools.widgets.tooltips import ToolTip


class ToolTips:
    """
    The ToolTips class. Responsible for initializing all tooltips for the main windows widgets.
    """

    def __init__(self, layout: Layout) -> None:
        """
        Inits the ToolTips class.

        Args:
            layout (Layout): The layout of the main window.
        """

        ToolTip(
            widget=layout.linked_document,
            text=(
                "The partnumber of the linked document. The linked document is the "
                "document from the first view in the current sheet."
            ),
        )

        ToolTip(
            widget=layout.button_reload_product,
            text="Reloads the product number from the linked document.",
        )

        ToolTip(
            widget=layout.button_reload_partnumber,
            text="Reloads the part number from the linked document.",
        )

        ToolTip(
            widget=layout.button_reload_revision,
            text="Reloads the revision number from the linked document.",
        )

        ToolTip(
            widget=layout.button_reload_definition,
            text="Reloads the definition from the linked document.",
        )

        ToolTip(
            widget=layout.button_reload_material,
            text="Reloads the material from the linked document.",
        )

        ToolTip(
            widget=layout.button_reload_base_size,
            text="Reloads the base size from the linked document.",
        )

        ToolTip(
            widget=layout.button_reload_tolerance,
            text="Reloads the tolerance from the linked document.",
        )

        ToolTip(
            widget=layout.button_save,
            text="Writes the input to the title block and closes the app.",
        )

        ToolTip(
            widget=layout.button_abort,
            text="Discards all changes and closes the app.",
        )

        ToolTip(
            widget=layout.toggle_symlink,
            text="Automatically uses relative workspace paths or symlinks to write the document path.",
        )
