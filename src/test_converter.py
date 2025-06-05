import unittest
from codesplit import *

class TestConverter(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_conv(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a *text* node", TextType.TEXT)
        nodes = [node, node2]
        #print(split_nodes_delimiter(nodes, "*", TextType.BOLD))

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)




if __name__ == "__main__":
    unittest.main()
