"""
    Tool for creating tolerance tables.
"""

from dataclasses import dataclass
from tkinter import messagebox as tkmsg
from typing import List

from const import (
    TOLERANCE_TABLE_CELL_HEIGHT,
    TOLERANCE_TABLE_CELL_WIDTH,
    TOLERANCE_TABLE_NAME,
)
from loader.doc_loader import DocumentLoader
from pytia.framework.drafting_interfaces.drawing_dimension import DrawingDimension
from pytia.framework.drafting_interfaces.drawing_table import DrawingTable
from pytia.log import log
from pytia.wrapper.documents.drawing_documents import PyDrawingDocument
from resources import resource


@dataclass(kw_only=True, slots=True, frozen=True)
class ToleranceTableModel:
    base: str
    min: str
    max: str


@dataclass(kw_only=True, slots=True, frozen=True)
class ToleranceModel:
    name: str
    value: float
    precision: float

    tol_type: int
    tol_name: str
    tol_up_s: str
    tol_low_s: str
    tol_up_d: float
    tol_low_d: float
    tol_display: int


class ToleranceTools:
    def __init__(self, doc_loader: DocumentLoader) -> None:
        self.doc = doc_loader
        self.views = doc_loader.views

    @staticmethod
    def prepare_table_data(
        tolerated_dimensions: List[ToleranceModel],
    ) -> List[ToleranceTableModel]:
        table_data: List[ToleranceTableModel] = []

        # Add table header
        table_data.append(ToleranceTableModel(base="Base", min="Min", max="Max"))

        # Add table data
        for item in tolerated_dimensions:
            base = f"{item.value:.3f} {item.tol_up_s}"
            min = f"{(item.value+item.tol_low_d):.4f}"
            max = f"{(item.value+item.tol_up_d):.4f}"

            # Don't add the same value twice
            for datum in table_data:
                if datum.base == base:
                    break

            table_data.append(
                ToleranceTableModel(
                    base=base,
                    min=min,
                    max=max,
                )
            )
        return table_data

    def get_all_tolerated_dimensions(self) -> List[ToleranceModel]:
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
        self.remove_table()

        dimensions = self.get_all_tolerated_dimensions()
        data = self.prepare_table_data(dimensions)

        if not data:
            tkmsg.showinfo(
                title=resource.settings.title,
                message="No dimension has tolerated values.",
            )
            return

        table = self.doc.background_view.tables.add(
            0, 0, len(data), 3, TOLERANCE_TABLE_CELL_HEIGHT, TOLERANCE_TABLE_CELL_WIDTH
        )
        table.name = TOLERANCE_TABLE_NAME

        for row, datum in enumerate(data):
            table.set_cell_string(row + 1, 1, datum.base)
            table.set_cell_string(row + 1, 2, str(datum.min))
            table.set_cell_string(row + 1, 3, str(datum.max))

            for col in range(3):
                cell = table.get_cell_object(row + 1, col + 1)
                cell.set_font_size(0, 0, 2)
                table.set_cell_alignment(row + 1, col + 1, 4)

    def remove_table(self) -> None:
        rm_index = None

        for index, table in enumerate(self.doc.background_view.tables):
            if table.name == TOLERANCE_TABLE_NAME:
                rm_index = index + 1

        if rm_index is not None:
            self.doc.background_view.tables.remove(rm_index)
