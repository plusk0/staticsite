from textnode import TextNode
from fixed_variables import *
import re
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        
        if node.text_type == TextType.TEXT and str(delimiter) in node.text:
            node_text = []
            node_text = node.text.split(delimiter,2)

            new_nodes.extend([TextNode(node_text[0],TextType.TEXT),TextNode(node_text[1],text_type)])
            if len(node_text) == 3:
                more_nodes = split_nodes_delimiter([TextNode(node_text[2],TextType.TEXT)], delimiter, text_type)
                for i in more_nodes:
                    new_nodes.append(i)
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):                          
    matches = re.findall(r"!\[.*?\)",text)              # Reference: https://regexr.com/
    tuples = []

    for match in matches:
        text = []
        text = str(re.findall(r"\[.*?\]",match))        # Possible improvement: use a simpler implementation
        text = re.sub(r"\[|\]|\(|\)|\'", "",text)       # for getting rid of ()[]'                                            # > using a list and removing first and last entry
        link = str(re.findall(r"\(.*?\)",match))
        link = re.sub(r"\[|\]|\(|\)|\'", "",link)
        image = (text, link)
        tuples.append(image)

    return tuples

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[.*?\)",text)
    tuples = []

    for match in matches:
        text = str(re.findall(r"\[.*?\]",match))
        text = re.sub(r"\[|\]|\(|\)|\'", "",text)
        link = str(re.findall(r"\(.*?\)",match))
        link = re.sub(r"\[|\]|\(|\)|\'", "",link)
        webpage = (text, link)
        tuples.append(webpage)
    return tuples

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
            if "![" in node.text:
                node_text = []
                node_text = node.text.split("!",1)
                new_nodes.append(TextNode(node_text[0],TextType.TEXT))
                node_text = node_text[1].split(")",1)
                tuples = extract_markdown_images("!" + node_text[0] + ")")
                new_nodes.append(TextNode(tuples[0][0],TextType.IMAGE,tuples[0][1]))    #error ?

                if "!" in node_text[1]:
                    more_nodes = split_nodes_image([TextNode(node_text[1],TextType.TEXT)])
                    for i in more_nodes:
                        new_nodes.append(i)
                else: new_nodes.append(TextNode(node_text[1], TextType.TEXT))
            else:
                new_nodes.append(node)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
            if "[" in node.text:
                node_text = []
                node_text = node.text.split("[",1)

                new_nodes.append(TextNode(node_text[0],TextType.TEXT))
                node_text = node_text[1].split(")",1)
                tuples = extract_markdown_links("[" + node_text[0] + ")")
                new_nodes.append(TextNode(tuples[0][0],TextType.LINK,tuples[0][1]))

                if "(" in node_text[1]:
                    more_nodes = split_nodes_link([TextNode(node_text[1],TextType.TEXT)])
                    for i in more_nodes:
                        new_nodes.append(i)
            else:
                new_nodes.append(node)
    for node in new_nodes:
        if node.text == "":
            new_nodes.remove(node)
    return new_nodes

def text_to_nodes(text):
    delimit_bold = split_nodes_delimiter([TextNode(text,TextType.TEXT)], "**", TextType.BOLD)
    delimit_italic = split_nodes_delimiter(delimit_bold, "_", TextType.ITALIC)
    delimit_code = split_nodes_delimiter(delimit_italic, "`", TextType.CODE)
    images = split_nodes_image(delimit_code)
    links = split_nodes_link(images)

    for node in links:
        if node.text == "":
            links.remove(node)
    return links

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(Text):

    if re.match(r"(^#{1,6} )(.+)",Text):
        
        return BlockType.HDG

    if re.findall(r"(^```.*```$)", Text, re.DOTALL) != []:
        
        return BlockType.CODE
    
    if re.match(r"^>.*", Text):
        if re.match(r"\n>", Text) == re.match(r"\n.", Text):

            return BlockType.QUOTE

    if re.match(r"^- ", Text):
        if re.match(r"\n- ", Text) == re.match(r"\n.", Text):
            return BlockType.LIST_U
    
    if re.match(r"^1", Text):
        x = 2
        list_line_nrs = re.findall(r"\n\d", Text, re.MULTILINE)
        for line_nr in list_line_nrs:
            if str(x) not in line_nr:
                return BlockType.PARA
            x += 1
        return BlockType.LIST_O
    else:
        return BlockType.PARA
    


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[3:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = raw_text_node.text_node_to_html_node()
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def text_to_children(text):
    Leaf_nodes = []
    text_nodes = text_to_nodes(text)
    Leaf_nodes = [x.text_node_to_html_node() for x in text_nodes]
    return Leaf_nodes


def create_html_nodes(markdown):
    block_list = markdown_to_blocks(markdown)
    HTML_nodes = []
    x = 1
    for block in block_list:
        types = block_to_block_type(block)
        match types:
            case BlockType.PARA:
                HTML_nodes.append(paragraph_to_html_node(block))
            case BlockType.HDG:

                HTML_nodes.append(heading_to_html_node(block))
            case BlockType.CODE:
                HTML_nodes.append(code_to_html_node(block))
            case BlockType.QUOTE:
                HTML_nodes.append(quote_to_html_node(block))
            case BlockType.LIST_U:
                HTML_nodes.append(ulist_to_html_node(block))
            case BlockType.LIST_O:
                HTML_nodes.append(olist_to_html_node(block))
            case _:
                raise ValueError("unknown block type")

    return HTML_nodes


def split_list_node(node):
    split = node.value.split("\n")
    children = []
    for line in split:
        children.append(LeafNode("li",line[2::])) # 2:: removes markdown line numbering
    return children


def markdown_to_html_node(markdown):
    html_nodes = create_html_nodes(markdown)
    nested_nodes = html_nodes
    parent = ParentNode("div",nested_nodes)
  
    return parent


    
            
