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


if __name__ == "__main__":
    unittest.main()