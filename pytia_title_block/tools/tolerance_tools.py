"""
    Tool for creating tolerance tables.
"""

from tkinter import messagebox as tkmsg
from typing import List

from const import (
    TOLERANCE_TABLE_CELL_HEIGHT,
    TOLERANCE_TABLE_CELL_WIDTH,
    TOLERANCE_TABLE_NAME,
)
from helper.translators import translate_paper_size
from loader.doc_loader import DocumentLoader
from models.tolerance_model import ToleranceModel, ToleranceTableModel
from resources import resource


class ToleranceTools:
    """
    This class provides methods to create a tolerance table.
    A tolerance table is a collection of all tolerated dimensions of the active sheet.
    """

    def __init__(self, doc_loader: DocumentLoader) -> None:
        """
        Inits the class.

        Args:
            doc_loader (DocumentLoader): The doc loader instance.
        """
        self.doc = doc_loader
        self.views = doc_loader.views

    @staticmethod
    def prepare_table_data(
        tolerated_dimensions: List[ToleranceModel],
    ) -> List[ToleranceTableModel]:
        """
        Moves data from the ToleranceModel to the ToleranceTableModel.
        Does some filtering and creates header cells.

        Args:
            tolerated_dimensions (List[ToleranceModel]): _description_

        Returns:
            List[ToleranceTableModel]: _description_
        """
        table_data: List[ToleranceTableModel] = []

        # Add table header
        table_data.append(
            ToleranceTableModel(
                base=resource.settings.tables.tolerances.header_base,
                min=resource.settings.tables.tolerances.header_min,
                max=resource.settings.tables.tolerances.header_max,
            )
        )

        # Add table data
        for item in tolerated_dimensions:
            base = f"{item.value:.3f} {item.tol_up_s}"
            min = f"{(item.value+item.tol_low_d):.4f}"
            max = f"{(item.value+item.tol_up_d):.4f}"

            # Don't add the same value twice
            add = True
            for datum in table_data:
                if datum.base == base:
                    add = False
            if add:
                table_data.append(ToleranceTableModel(base=base, min=min, max=max))

        return table_data

    def get_all_tolerated_dimensions(self) -> List[ToleranceModel]:
        """
        Returns all dimensions that have a tolerated value of type `2`.

        Returns:
            List[ToleranceModel]: All tolerated dimensions.
        """
        dimensions = []
        for view_index in range(1, self.views.count + 1):
            for dim_index in range(1, self.views.item(view_index).dimensions.count + 1):
                dimension = self.views.item(view_index).dimensions.item(dim_index)
                (
                    tol_type,
                    tol_name,
                    tol_up_s,
                    tol_low_s,
                    tol_up_d,
                    tol_low_d,
                    tol_display,
                ) = dimension.get_tolerances()

                # Tolerance type 2 means tolerated with iso value.
                if tol_type == 2:
                    dimensions.append(
                        ToleranceModel(
                            name=dimension.get_value().name,
                            value=dimension.get_value().value,
                            precision=dimension.get_value().get_format_precision(1),
                            tol_type=tol_type,
                            tol_name=tol_name,
                            tol_up_s=tol_up_s,
                            tol_low_s=tol_low_s,
                            tol_up_d=tol_up_d,
                            tol_low_d=tol_low_d,
                            tol_display=tol_display,
                        )
                    )
        return dimensions

    def add_table(self) -> None:
        """
        Adds the table to the sheet's background view according to the config of the settings.json.
        Removes existing tolerance tables first.
        """
        self.remove_table()

        dimensions = self.get_all_tolerated_dimensions()
        data = self.prepare_table_data(dimensions)

        if not data:
            tkmsg.showinfo(
                title=resource.settings.title,
                message="No dimension has tolerated values.",
            )
            return

        paper_size = translate_paper_size(self.doc.sheets.active_sheet.paper_size)
        table_x = 0
        table_y = 0
        for position in resource.settings.tables.tolerances.positions:
            if position.size == paper_size:
                table_x = position.x - 3 * TOLERANCE_TABLE_CELL_WIDTH
                table_y = position.y + len(data) * TOLERANCE_TABLE_CELL_HEIGHT
                break

        # Add the table to the sheet
        table = self.doc.background_view.tables.add(
            table_x,
            table_y,
            len(data),
            3,
            TOLERANCE_TABLE_CELL_HEIGHT,
            TOLERANCE_TABLE_CELL_WIDTH,
        )
        table.name = TOLERANCE_TABLE_NAME

        # Fill the table with the data
        for row, datum in enumerate(data):
            table.set_cell_string(row + 1, 1, datum.base)
            table.set_cell_string(row + 1, 2, str(datum.min))
            table.set_cell_string(row + 1, 3, str(datum.max))

            for col in range(3):
                cell = table.get_cell_object(row + 1, col + 1)
                cell.set_font_size(0, 0, 2)
                table.set_cell_alignment(row + 1, col + 1, 4)

        # Fit the notes above the table
        notes = self.doc.get_text_by_name(resource.title_block_items.notes)
        if notes and notes.y < table_y + 2.5:
            notes.y = table_y + 2.5

    def remove_table(self) -> None:
        """Removes existing tolerance tables."""
        rm_index = None

        for index, table in enumerate(self.doc.background_view.tables):
            if table.name == TOLERANCE_TABLE_NAME:
                rm_index = index + 1

        if rm_index is not None:
            self.doc.background_view.tables.remove(rm_index)
