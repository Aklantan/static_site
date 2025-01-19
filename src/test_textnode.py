import unittest

from textnode import TextNode, TextType,text_node_to_html_node



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_txt(self):
        node = TextNode("This is a node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is a node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_diff(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "www.bungie.com")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_raw(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(text_node_to_html_node(node).to_html(),"This is a text node")

    def test_text_node_to_html_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node).to_html(),"<b>This is a text node</b>")

    def test_text_node_to_html_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node).to_html(),"<i>This is a text node</i>")

    def test_text_node_to_html_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(text_node_to_html_node(node).to_html(),"<code>This is a text node</code>")

    def test_text_node_to_html_link(self):
        node = TextNode("This is a text node", TextType.LINK, url="www.google.com")
        self.assertEqual(text_node_to_html_node(node).to_html(),"<a href=\"www.google.com\">This is a text node</a>")
    
    def test_text_node_to_html_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, url="www.piccies.com")
        self.assertEqual(text_node_to_html_node(node).to_html(),"<img src=\"www.piccies.com\" alt=\"This is a text node\">")



if __name__ == "__main__":
    unittest.main()