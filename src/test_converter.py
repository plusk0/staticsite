import unittest
from codesplit import *
from fixed_variables import TextType

class TestConverter(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_images(self):
        if 1 == 2:
            matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        if 1 == 2:
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode(
                        "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                    ),
                ],
                new_nodes,
            )


    def test_split(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_nodes(node)
        self.assertListEqual(
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
,
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_to_block_type(self):
        lst_block= """1 Explore results with the Tools below. 
2 Replace & List output custom results. 
3 Details lists capture groups. 
4 Explain describes your expression in plain English."""
        self.assertEqual(block_to_block_type(lst_block),BlockType.LIST_O)

        code_block= """```1 Explore results with the Tools below. 
2 Replace & List output custom results. 
3 Details lists capture groups. 
4 Explain describes your expression in plain English.```"""
        self.assertEqual(block_to_block_type(code_block),BlockType.CODE)

        quote_block= """>1 Explore results with the Tools below. 
> Replace & List output custom results. 
> Details lists capture groups. 
> Explain describes your expression in plain English.```"""
        self.assertEqual(block_to_block_type(quote_block),BlockType.QUOTE)

        unordered= """- 1 Explore results with the Tools below. 
- Replace & List output custom results. 
- Details lists capture groups. 
- Explain describes your expression in plain English.```"""
        self.assertEqual(block_to_block_type(unordered),BlockType.LIST_U)

        hdg= """#### 1 Explore results with the Tools below. 
> Replace & List output custom results. 
- Details lists capture groups. 
> Explain describes your expression in plain English.```"""
        self.assertEqual(block_to_block_type(hdg),BlockType.HDG)

if __name__ == "__main__":
    unittest.main()
