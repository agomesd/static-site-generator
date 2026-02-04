import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_text_node_to_html_node_invalid_text_type(self):
        node = TextNode("This is a text node", "INVALID")
        with self.assertRaises(Exception):
            html_node = node.text_node_to_html_node()

    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_anchor(self):
        node = TextNode(
            "This is an anchor node", TextType.ANCHOR, "http://www.test.com"
        )
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is an anchor node")
        self.assertEqual(html_node.props_to_html(), ' href="http://www.test.com"')

    def test_text_node_to_html_node_bold(self):
        node = TextNode(
            "This is a bold text node",
            TextType.BOLD,
        )
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_text_node_to_html_node_italic(self):
        node = TextNode(
            "This is an italic text node",
            TextType.ITALIC,
        )
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_text_node_to_html_node_code(self):
        node = TextNode(
            "This is a code text node",
            TextType.CODE,
        )
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_text_node_to_html_node_img(self):
        node = TextNode(
            "This is an img text node", TextType.IMAGE, "https://www.test.com/img_1"
        )
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props_to_html(),
            ' src="https://www.test.com/img_1" alt="This is an img text node"',
        )

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode(
            "This is another text node", TextType.BOLD, "https://example.com"
        )
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
