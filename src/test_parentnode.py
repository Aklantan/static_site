import unittest

from htmlnode import ParentNode,LeafNode

class TestParentNode(unittest.TestCase):
    def test_props_to_html_no_children(self):
        # Test with None props
        node = ParentNode(tag = "ok", children=None)
        with self.assertRaises( ValueError):
            node.to_html()

    def test_props_to_html_no_tags(self):
        # Test with None props
        node = ParentNode(tag = None, children=[LeafNode("b", "Bold text")])
        with self.assertRaises( ValueError):
            node.to_html()

    def test_props_to_html_multiple_children(self):
        # Test with None props
        node = ParentNode(tag = "p", children=[
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_props_to_html_nested_parents(self):
        # Test with None props
        node = ParentNode(tag = "p", children=[
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        ParentNode(tag = "p", children=[
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ]),
        LeafNode(None, "Normal text"),
        ])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>Normal text</p>")





if __name__ == "__main__":
    unittest.main()