import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):

    def test_node(self):
        node = HTMLNode(None, None, "some","some")
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


if __name__ == "__main__":
    unittest.main()
