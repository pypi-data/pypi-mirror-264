# TypeScript Font Converter

Converts fonts to TypeScript objects

This library:
 - Imports OpenType and TrueType fonts
 - Extracts metadata from the naming table
 - Extracts a list of glyphs and their unicode character ID
 - Encodes the font file as a base64-encoded DataURI
 - Saves all this in Python objects
 - Serializes the Python Objects in a JSON file
 - Exports TypeScript definitions of the objects

## But Why?

This library exists to embed fonts into web pages using SSR-frameworks such as Next.js and to more easily gain information about the font.

It was initially part of the [ThorType](https://www.thortype.com) website where I use the TypeScript definition and the corresponding JSON-data to showcase my fonts and save all of that data as part of a static website.

It's released as a Python lib so that the tooling for the ThorType-website is separated and generalised to be reused in any TypeScript or JavaScript web framework.
