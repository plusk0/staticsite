import unittest
from codesplit import *

class TestConverter(unittest.TestCase):

    def test_conv(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a *text node", TextType.TEXT)
        nodes = [node, node2]
        print(split_nodes_delimiter(nodes, "*", TextType.BOLD))
        #self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
