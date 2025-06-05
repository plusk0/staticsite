from textnode import TextNode
from fixed_variables import TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    #print(old_nodes)
    for node in old_nodes:
        if node.text_type == TextType.TEXT and delimiter in node.text:
            node_text = []
            node_text = node.text.split(delimiter,2)
            new_nodes.extend([TextNode(node_text[0],TextType.TEXT),TextNode(node_text[1],text_type)])
            if len(node_text) == 3:
                newnode3 = split_nodes_delimiter([TextNode(node_text[2],TextType.TEXT)], delimiter, text_type)
                for i in newnode3:
                    new_nodes.append(i)
        else:
            new_nodes.append(node)

    return new_nodes

