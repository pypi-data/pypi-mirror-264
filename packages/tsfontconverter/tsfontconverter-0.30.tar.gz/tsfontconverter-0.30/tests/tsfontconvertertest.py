from src.tsfontconverter.fontparser.reflectionutils import get_typescript_definitions
from src.tsfontconverter.tsfontconverter import create_font_list
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

FONTDIRPATH = os.getenv("FONTDIRPATH")
FONT_LIST_PATH = os.getenv("FONT_LIST_PATH")
TYPEDEF_PATH = os.getenv("TYPEDEF_PATH")

FONT_LIST_DATA_START = '''import { Font } from "./font";

const fonts: Font[] = '''


def test_tsfontconverter():
    json_data = create_font_list(fontdirpath=FONTDIRPATH)
    with open(FONT_LIST_PATH, "w") as tsfile:
        tsfile.write(FONT_LIST_DATA_START)
        tsfile.write(json_data)

    typescript_definitions = get_typescript_definitions()
    with open(TYPEDEF_PATH, "w") as tsfile:
        for clazz_name in typescript_definitions:
            typescript_definition = typescript_definitions[clazz_name]
            tsfile.write(typescript_definition)
            tsfile.write("\n\n")
