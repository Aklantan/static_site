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
        # print("\nExpected:", expected)
        # print("Got:", result)
        # print("\nExpected[0]:", repr(expected[0]))
        # print("Got[0]:", repr(result[0]))
        
        self.assertEqual(result, expected)

class TestBlockToBlocks(unittest.TestCase):
    def test_block_to_blocks_paragraphs(self):
        # Test for a paragraph
        block = "This is a paragraph"
        assert block_to_block_type(block) == "paragraph"
        #Test for a multi-line paragraph
        block = """This is a paragraph
        Here is some more text
        More paragraph"""
        assert block_to_block_type(block) == "paragraph"
        #Test for empty string
        block = ""
        assert block_to_block_type(block) == "paragraph"

    def test_block_to_blocks_headings(self):
        #Tests for each number of # possible for a heading
        block = "# This is a heading"
        assert block_to_block_type(block) == "heading"
        block = "## This is a heading"
        assert block_to_block_type(block) == "heading"
        block = "### This is a heading"
        assert block_to_block_type(block) == "heading"
        block = "#### This is a heading"
        assert block_to_block_type(block) == "heading"
        block = "##### This is a heading"
        assert block_to_block_type(block) == "heading"
        block = "###### This is a heading"
        assert block_to_block_type(block) == "heading"
        block = "####### This is a heading"
        assert block_to_block_type(block) == "paragraph"

    def test_block_to_blocks_code(self):
        block = """``` ls -lh```"""
        assert block_to_block_type(block) == "paragraph"
        block = """``` ls -lh
        ```"""
        assert block_to_block_type(block) == "code"
        block = """```
        ```"""
        assert block_to_block_type(block) == "code"

    def test_block_to_blocks_quote(self):
        block = ">Goddamn I love these peaches"
        assert block_to_block_type(block) == "quote"
        block = """>Goddamn I love these peaches
        Oh yea"""
        assert block_to_block_type(block) == "quote"

    def test_block_to_blocks_unordered_list(self):
        block = """* Item 1
- Item 2
* Item 3"""
        assert block_to_block_type(block) == "unordered_list"

        block = """* Item 1
- Item 2
 Item 3"""
        assert block_to_block_type(block) == "paragraph"  

    def test_block_to_blocks_unordered_list(self):
        block = """1. Item 1
2. Item 2
3. Item 3"""
        assert block_to_block_type(block) == "ordered_list"

        block = """1. Item 1
2. Item 2
4. Item 3"""
        assert block_to_block_type(block) == "paragraph"  


class TestMarkdowntoHTMLNode(unittest.TestCase):
    def test_quote_block(self):
        markdown = "> This is a quote\n> spanning multiple lines\n> with some **bold** text\n> and a > character inside"
        node = markdown_to_html_node(markdown)
        # The result should be a div containing a blockquote
        # The blockquote should contain the text without > markers
        # The **bold** text should be properly converted to <strong>
        print("Generated:", node.to_html())
        print("Expected:", "<div><blockquote>This is a quote\nspanning multiple lines\nwith some <strong>bold</strong> text\nand a > character inside</blockquote></div>")
        expected_html = "<div><blockquote>This is a quote\nspanning multiple lines\nwith some <strong>bold</strong> text\nand a > character inside</blockquote></div>"
        assert node.to_html() == expected_html


class TestTitleExtract(unittest.TestCase):
    def test_title_extract(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown),"Hello")
        markdown = "Some text\n# Title\nMore text"
        assert extract_title(markdown) == "Title"
        markdown = "No title here"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception),"No title in document")





if __name__ == "__main__":
    unittest.main()