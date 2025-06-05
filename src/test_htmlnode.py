import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):

    def test_node(self):
        node = HTMLNode("tag", "value", "children","props")
        print(node)

    def test_props(self):
        node = HTMLNode(None, None, "some",{
        "href": "https://www.google.com",
        "target": "_blank",
        })
        print(node.props_to_html())

    def test_to_html(self):
        node = HTMLNode(None, "None", "some","some")
        

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        print(node.to_html())
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
