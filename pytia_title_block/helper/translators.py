"""
    Translators helper functions
"""


def translate_paper_size(size: int) -> str:
    sizes = {6: "A4", 5: "A3", 4: "A2", 3: "A1", 2: "A0"}
    return sizes[size]
