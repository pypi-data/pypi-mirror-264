from dataclasses import dataclass


@dataclass
class Glyph():
    glyphId: int = -1
    unicode: str = ""
