import unittest

from leafnode import LeafNode


class TestLeadNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.example.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.example.com">Click me!</a>'
        )

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode(
            "p", "Hello, world!", {"class": "paragraph", "style": "color:black"}
        )
        self.assertEqual(
            node.to_html(), '<p class="paragraph" style="color:black">Hello, world!</p>'
        )

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is simply a text node", None)
        self.assertEqual(node.to_html(), "This is simply a text node")
