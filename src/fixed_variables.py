from enum import Enum
import sys
import pathlib

basepath = sys.argv

if len(basepath) > 1:
    print("path:",basepath[1])
    basepath = basepath[1]
else:
    basepath = "/"


source = "./content"                
static = "./src/static"               # static content
#dest = "./public"              # public folder for local testing
dest =  "./docs"                 # docs folder for github
markdown_path = "./content"          # template + main index md-file


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

