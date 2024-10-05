import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    html_node = HTMLNode(
        tag="a",
        value="This is some text",
        props={"href": "https://www.boot.dev", "target": "_blank"},
    )

    def test_init(self):
        self.assertEqual(self.html_node.tag, "a")
        self.assertEqual(self.html_node.value, "This is some text")
        self.assertTrue(self.html_node.children is None)
        self.assertEqual(
            self.html_node.props, {"href": "https://www.boot.dev", "target": "_blank"}
        )

    def test_to_html(self):
        with self.assertRaises(NotImplementedError):
            self.html_node.to_html()

    def test_props_to_html(self):
        html_props = self.html_node.props_to_html()
        self.assertEqual(html_props, ' href="https://www.boot.dev" target="_blank"')

    def test_repr(self):
        self.assertEqual(
            self.html_node.__repr__(),
            f"HTMLNode({self.html_node.tag}, {self.html_node.value}, {self.html_node.children}, {self.html_node.props})",
        )

    def test_eq(self):
        other_node = HTMLNode(
            tag="a",
            value="This is some text",
            props={"href": "https://www.boot.dev", "target": "_blank"},
        )
        self.assertTrue(self.html_node, other_node)


class TestLeafNode(unittest.TestCase):
    leaf_node = LeafNode(
        tag="p",
        value="This is some text",
        props={"target": "_blank"},
    )

    def test_init(self):
        self.assertEqual(self.leaf_node.tag, "p")
        self.assertEqual(self.leaf_node.value, "This is some text")
        self.assertEqual(self.leaf_node.props, {"target": "_blank"})

    def test_to_html(self):
        html = self.leaf_node.to_html()
        self.assertEqual(html, '<p target="_blank">This is some text</p>')


class TestParentNode(unittest.TestCase):
    parent_node = ParentNode(
        tag="p",
        children=[
            LeafNode("Bold text", "b"),
            LeafNode("Normal text"),
            LeafNode("italic text", "i"),
            LeafNode("Normal text"),
        ],
    )

    def test_init(self):
        self.assertEqual(self.parent_node.tag, "p")
        self.assertListEqual(
            self.parent_node.children,
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text"),
                LeafNode("italic text", "i"),
                LeafNode("Normal text"),
            ],
        )

    def test_to_html(self):
        self.assertEqual(
            self.parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_nested_parents(self):
        nested_parent_node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    "p",
                    [
                        LeafNode("Bold text", "b"),
                        LeafNode("Normal text"),
                        LeafNode(
                            "this is a link", "a", {"href": "https://www.boot.dev"}
                        ),
                    ],
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode("Normal text"),
                        LeafNode("italic text", "i"),
                        LeafNode("Normal text"),
                    ],
                ),
            ],
        )
        self.assertEqual(
            nested_parent_node.to_html(),
            '<div><p><b>Bold text</b>Normal text<a href="https://www.boot.dev">this is a link</a></p><p>Normal text<i>italic text</i>Normal text</p></div>',
        )

    def test_to_html_with_no_children(self):
        childless_parent_node = ParentNode(
            tag="p",
            children=[],
        )
        self.assertEqual(childless_parent_node.to_html(), "<p></p>")
