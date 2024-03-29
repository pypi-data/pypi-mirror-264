"""
Classes and methods that are used by multiple report tables.
"""

from enum import Enum


class TableColor(Enum):
    """
    Hexadecimal representations of RGB colors used in the report tables.
    """

    WHITE = "#FFFFFF"
    BLACK = "#000000"
    GRAY = "#5A6E8C20"
    DARK_GRAY = "#5A6E8C"
    LIGHT_GRAY = "#A7B9D120"
    YELLOW = "#E0C051"
    ORANGE = "#DD7E38"
    RED = "#992D3C"
