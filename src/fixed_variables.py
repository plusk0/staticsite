from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARA = "paragraph"
    HDG = "heading"
    CODE = "code"
    QUOTE = "quote"
    LIST_U = "unordered_list"
    LIST_O = "ordered_list"

