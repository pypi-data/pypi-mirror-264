from dataclasses import dataclass, field

from .CharacterMap import CharacterMap
from .FontStandard import FontStandard
from .Meta import Meta


@dataclass
class Font():
    name: str = ""
    meta: Meta = field(default_factory=Meta)
    characterMap: CharacterMap = field(default_factory=CharacterMap)
    type: FontStandard = FontStandard.OpenType
    dataUri: str = ""

    def to_dict(self):
        meta = Meta().__dict__ if self.meta is None else self.meta.__dict__
        characterMap = CharacterMap().to_dict() if self.characterMap is None else self.characterMap.to_dict()
        myType = "" if self.type is None else str(self.type)
        return {
            "name": self.name,
            "meta": meta,
            "type": myType,
            "characterMap": characterMap,
            "dataUri": self.dataUri,
        }
