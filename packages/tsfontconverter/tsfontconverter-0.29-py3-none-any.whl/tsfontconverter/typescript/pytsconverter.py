from typing import Dict

TYPE_MAP: Dict[str, str] = {
    "bool": "boolean",
    "str": "string",
    "int": "number",
    "float": "number",
    "complex": "number",
    "Any": "any",
    "Dict": "Record<any, any>",
    "List": "any[]",
    "Tuple": "[any]",
    "Union": "any",
}

SUBSCRIPT_FORMAT_MAP: Dict[str, str] = {
    "Dict": "Record<{0}>",
    "List": "{0}[]",
    "Optional": "{0} | null",
    "Tuple": "[{0}]",
    "Union": "{0}",
}


def convert_regular_type(pytype):
    if pytype in TYPE_MAP.keys():
        return TYPE_MAP[pytype]
    else:
        return pytype


def convert_subscript_type(pytype, subsripttype):
    if pytype in SUBSCRIPT_FORMAT_MAP.keys():
        return SUBSCRIPT_FORMAT_MAP[pytype].format(subsripttype)
    else:
        return pytype

