#/usr/bin/python3

from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PG = "paragraph"
    HEAD = "header"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered list"
    OL = "ordered list"
