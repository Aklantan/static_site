import unittest

from textnode import TextNode, TextType,text_node_to_html_node
from markdown_totextnodes import *


class TestMarkdowntoTextNode(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes,  [
    TextNode("This is text with a link ", TextType.TEXT),
    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
    TextNode(" and ", TextType.TEXT),
    TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
])

class TestMarkdowntoTextNode(unittest.TestCase):
    def test_split_nodes_images(self):
        node = TextNode(
    "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes,  [
    TextNode("This is text with a link ", TextType.TEXT),
    TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
    TextNode(" and ", TextType.TEXT),
    TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
])
class TestTexttoTextNode(unittest.TestCase):
    def test_text_to_textnodes(self):
        # Test 1: Basic delimiter test
        text1 = "This is **bold** and *italic*"
        nodes1 = text_to_textnodes(text1)
        # What do you expect the length of nodes1 to be?
        
        # Test 2: Mixed delimiters with links
        text2 = "This is a [link](https://boot.dev) and some `code`"
        nodes2 = text_to_textnodes(text2)
        
        # Test 3: Image test
        text3 = "Here's an ![image](https://image.url)"
        nodes3 = text_to_textnodes(text3)
        
        # Test 4: Empty string
        text4 = ""
        nodes4 = text_to_textnodes(text4)
class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # Test 1: Basic blocks with single separator
        assert markdown_to_blocks("Block 1\n\nBlock 2") == ["Block 1", "Block 2"]

        # Test 2: Multiple blank lines between blocks
        assert markdown_to_blocks("Block 1\n\n\n\nBlock 2") == ["Block 1", "Block 2"]

        # Test 3: List items (should stay together)
        assert markdown_to_blocks("# Heading\n\n* Item 1\n* Item 2") == ["# Heading", "* Item 1\n* Item 2"]

        # Test 4: Whitespace handling
        assert markdown_to_blocks("  Block 1  \n\n  Block 2  ") == ["Block 1", "Block 2"]

        # Test 5: Complex markdown (like from the example)
        test_md = """# This is a heading

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is the first list item in a list block
    * This is a list item
    * This is another list item"""
        
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        result = markdown_to_blocks(test_md)
        print("Expected:", expected)
        print("Got:", result)
        assert result == expected

        print("All tests passed!")

if __name__ == "__main__":
    unittest.main()