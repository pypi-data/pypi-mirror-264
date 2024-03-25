from dataclasses import dataclass, field
from typing import List

from .Glyph import Glyph


@dataclass
class CharacterMap():
    glyphs: List[Glyph] = field(default_factory=list)

    # Only used for introspection
    numberOfGlyphs: int = 0

    def to_dict(self):
        glyphs = [] if self.glyphs is None else [glyph.__dict__ for glyph in self.glyphs]
        return {
            "glyphs": glyphs,
            "numberOfGlyphs": len(glyphs)
        }
