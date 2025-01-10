import unittest

from htmlnode import HTMLNode

def TestHTMLNode(unittest,TestCase):
    def test_props_to_html_none(self):
        # Test with None props
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        # Test with single property
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\"")

    def test_props_to_html_multiple(self):
        # Test with multiple properties
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank" })
        self.assertEqual(node.props_to_html(), "href=\"https://www.google.com\" target=\"_blank\"")




if __name__ == "__main__":
    unittest.main()