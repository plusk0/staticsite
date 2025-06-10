from enum import Enum

root = "/home/desktop/workspace/staticsite"

source = root + "/src/static"       # static content
dest = root + "/public"             # public folder
markdown_path = root + "/content"   # template + main index md-file


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

