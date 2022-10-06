from dataclasses import dataclass


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
