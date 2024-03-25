from dataclasses import dataclass


@dataclass
class Glyph:
    glyphId: str = ""
    unicode: int = -1
