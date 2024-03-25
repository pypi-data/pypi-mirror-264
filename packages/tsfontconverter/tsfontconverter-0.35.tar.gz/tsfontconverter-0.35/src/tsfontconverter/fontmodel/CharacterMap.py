from dataclasses import dataclass, field
from typing import List

from .Glyph import Glyph


@dataclass
class CharacterMap:
    # Only used for introspection
    numberOfGlyphs: int = 0

    glyphs: List[Glyph] = field(default_factory=list)

    def to_dict(self):
        glyphs = [] if self.glyphs is None else [glyph.__dict__ for glyph in self.glyphs]
        return {
            "numberOfGlyphs": len(glyphs),
            "glyphs": glyphs
        }
