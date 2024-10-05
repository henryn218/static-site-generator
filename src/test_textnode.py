import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_init(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertEqual(node.url, "https://www.boot.dev")

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(
            node.__repr__(),
            "TextNode(This is a text node, TextType.BOLD, https://www.boot.dev)",
        )

    def test_init_with_url_set_to_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertIsNone(node.url)

    def test_eq_with_inequality(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_repr_with_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(
            node.__repr__(), "TextNode(This is a text node, TextType.BOLD, None)"
        )


class TestTextNodeToLeafNode(unittest.TestCase):
    def test_bold_text_node_to_html_node(self):
        text_node = TextNode("Here is some text", TextType.BOLD)
        leaf_node = LeafNode("Here is some text", "b")
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_image_text_node_to_html_node(self):
        text_node = TextNode(
            "Here is an image", TextType.IMAGE, "https://www.image.img"
        )
        leaf_node = LeafNode(
            "",
            "img",
            {"src": "https://www.image.img", "alt": "Here is an image"},
        )
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_link_text_node_to_html_node(self):
        text_node = TextNode("Here is a link", TextType.LINK, "https://www.image.img")
        leaf_node = LeafNode(
            "Here is a link",
            "a",
            {"href": "https://www.image.img"},
        )
        self.assertEqual(text_node_to_html_node(text_node), leaf_node)

    def test_unknown_type_text_node_to_html_node(self):
        text_node = TextNode("Here is a link", "text_type", "https://www.image.img")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()
