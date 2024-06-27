from dataclasses import dataclass
from enum import Enum


class FontEnum(Enum):
    HELV = "helv"
    HELV_BOLD = "helv_Bold"
    HELV_OBLIQUE = "helv_Oblique"
    HELV_BOLDOBLIQUE = "helv_BoldOblique"
    TIMES = "times"
    TIMES_BOLD = "times_Bold"
    TIMES_ITALIC = "times_Italic"
    TIMES_BOLDITALIC = "times_BoldItalic"
    COUR = "cour"
    COUR_BOLD = "cour_Bold"
    COUR_OBLIQUE = "cour_Oblique"
    COUR_BOLDOBLIQUE = "cour-BoldOblique"
    SYMBOL = "symbol"
    ZAPFDINGBATS = "zapfdingbats"

@dataclass
class DocumentSize:
    width : int
    height : int

class DocumentSizeEnum(Enum):
    A3 = DocumentSize(width=842 , height=1191)
    A4 = DocumentSize(width=595, height=842)
    A5 = DocumentSize(width=420 , height=595)

class FontSizeEnum(Enum):
    BODY_SMALL = 8
    BODY_MEDIUM = 10
    BODY_LARGE = 12
    SUBHEADING = 14
    HEADING = 20
    TITLE = 24

class DocumentStyleEnum(Enum):
    GRID2COLS = "GRID2COLS" # TODO: To be implemented
    GRID3COLS = "GRID3COLS" # TODO: To be implemented
    LINEAR = "LINEAR"

@dataclass
class DocumentSection:
    content : str
    font : FontEnum
    font_size : FontSizeEnum
    text_color : tuple[int, int, int]
