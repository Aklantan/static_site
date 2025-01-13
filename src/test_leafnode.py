import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_props_to_html_single(self):
        # Test with no property and no tag
        node = LeafNode( "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "This is a paragraph of text")

    def test_props_to_html_single(self):
        # Test with no properties
        node = LeafNode("p", "This is a paragraph of text.")
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_props_to_html_single(self):
        # Test with a single property
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")




if __name__ == "__main__":
    unittest.main()