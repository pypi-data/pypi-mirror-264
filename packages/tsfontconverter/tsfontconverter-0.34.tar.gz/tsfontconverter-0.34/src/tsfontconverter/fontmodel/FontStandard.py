from enum import Enum


def toFontStandard(suffix: str):
    if suffix == ".otf":
        return FontStandard.OpenType
    if suffix == ".ttf":
        return FontStandard.TrueType
    return None


class FontStandard(Enum):
    OpenType = 'OpenType'
    TrueType = 'TrueType'
