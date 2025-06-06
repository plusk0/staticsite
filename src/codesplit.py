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
            if "!" in node.text:
                node_text = []
                node_text = node.text.split("!",1)
                new_nodes.append(TextNode(node_text[0],TextType.TEXT))
                node_text = node_text[1].split(")",1)
                tuples = extract_markdown_images("!" + node_text[0] + ")")
                new_nodes.append(TextNode(tuples[0][0],TextType.IMAGE,tuples[0][1]))

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
    blocklist = []
    if "\n\n" in markdown:
        paragraph, rest = markdown.split("\n\n", 1)
        if paragraph != "":
            blocklist.append(paragraph.strip())
        blocklist.extend(markdown_to_blocks(rest))
    elif markdown != "":
        blocklist.append(markdown)
    return blocklist

def block_to_block_type(Text):
    if re.match(r"(^#{1,6} )(.+)",Text):
        return BlockType.HDG
    
    if re.match(r"(^```.*```$)", Text, re.DOTALL):
        return BlockType.CODE
    
    if re.match(r"^>.*", Text):
        if re.match(r"\n>", Text) == re.match(r"\n.", Text):
            return BlockType.QUOTE

    if re.match(r"^- ", Text):
        if re.match(r"\n- ", Text) == re.match(r"\n.", Text):
            return BlockType.LIST_U
    
    if re.match(r"^1", Text):
        x = 2
        for line_nr in re.findall(r"\n\d", Text, re.MULTILINE):
            if str(x) not in line_nr:
                return BlockType.PARA
            x += 1
        return BlockType.LIST_O
    else:
        return BlockType.PARA
    
def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    for block in block_list:
        type = block_to_block_type(block)
        match type:
            case BlockType.LIST_U:
                return
