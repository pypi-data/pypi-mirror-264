from .fontparser.fontparser import FontParser

def main():
    """Entry point for the application script"""
    print("TSFontConverter entrypoint main")


def convert_font(font):
    # Add your font conversion logic here
    print("converting font: {font}".format(font=str(font)))


def create_font_list(fontdirpath):
    fontparser = FontParser(fontdirpath=fontdirpath)
    return fontparser.list_font_files()


