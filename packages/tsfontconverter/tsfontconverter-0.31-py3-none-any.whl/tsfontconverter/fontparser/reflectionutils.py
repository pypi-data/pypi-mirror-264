import inspect
import json
from enum import Enum

from ..fontmodel.CharacterMap import CharacterMap
from ..fontmodel.Font import Font
from ..fontmodel.FontStandard import FontStandard
from ..fontmodel.Glyph import Glyph
from ..fontmodel.Meta import Meta

from ..typescript.pytsconverter import convert_subscript_type
from ..typescript.pytsconverter import convert_regular_type


def get_typescript_definitions():
    return get_all_definitions()


def is_enum(cls):
    return inspect.isclass(cls) and issubclass(cls, Enum)


def get_class_definition(clazz):
    fontClassDefinition = inspect.signature(clazz.__init__)
    fontDict = {}

    if is_enum(clazz):
        print(f"{clazz.__name__} is an enum")
        enum_str = f"export enum {clazz.__name__} {{\n"
        for index, member in enumerate(clazz):
            if index < len(clazz) - 1:
                enum_str += f"  {member.name},\n"
            else:
                enum_str += f"  {member.name}\n"
        enum_str += "}"
        return enum_str

    for param_name, param in fontClassDefinition.parameters.items():
        if param_name is not "self":
            param_type = param.annotation
            if hasattr(param_type, "__origin__") and param_type.__origin__ == list:
                list_item_type = param_type.__args__[0].__name__
                tstype = convert_subscript_type(pytype=param.annotation.__name__, subsripttype=str(list_item_type))
                fontDict[param_name] = str(tstype)
            else:
                tstype = convert_regular_type(param.annotation.__name__)
                fontDict[param_name] = str(tstype)
    return f"export interface {clazz.__name__} {json.dumps(fontDict, indent=2).replace("\"", "")}"


def get_all_definitions():
    tsdefinitions = {}
    for cls in [FontStandard, Glyph, CharacterMap, Meta, Font]:
        tsdefinitions[cls.__name__] = get_class_definition(cls)
    return tsdefinitions
