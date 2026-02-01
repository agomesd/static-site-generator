import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "p", "This is a p tag", None, {"class": "paragraph", "style": "color:black"}
        )

        test = node.props_to_html()
        self.assertEqual(test, ' class="paragraph" style="color:black"')
        node = HTMLNode("p", "This is a p tag", None, None)
        test = node.props_to_html()
        self.assertEqual(test, "")
