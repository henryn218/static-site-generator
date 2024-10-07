import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)
from htmlnode import ParentNode, LeafNode


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        actual = markdown_to_blocks(
            """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block\n* This is a list item\n* This is another list item
            """
        )
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(actual, expected)

    def test_markdown_to_blocks_with_more_than_two_line_breaks(self):
        actual = markdown_to_blocks(
            """
            # This is a heading



            This is a paragraph of text. It has some **bold** and *italic* words inside of it.


            * This is the first list item in a list block\n* This is a list item\n* This is another list item
            """
        )
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(actual, expected)

    def test_markdown_to_blocks_with_empty_string(self):
        actual = markdown_to_blocks("")
        self.assertEqual(actual, [])

    def test_markdown_to_blocks_with_no_line_breaks(self):
        actual = markdown_to_blocks("hello world")
        self.assertEqual(actual, ["hello world"])

    def test_single_block(self):
        actual = markdown_to_blocks(
            "This is a single block\nwith multiple lines\nbut no empty lines"
        )
        expected = ["This is a single block\nwith multiple lines\nbut no empty lines"]
        self.assertEqual(actual, expected)

    def test_block_to_block_type_with_heading(self):
        self.assertEqual(block_to_block_type("###### This is a heading"), "heading")

    def test_block_to_block_type_with_code(self):
        self.assertEqual(block_to_block_type("```This is code\n```"), "code")

    def test_block_to_block_type_with_unordered_list(self):
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), "unordered_list")

    def test_block_to_block_type_with_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. item 1\n2. item 2\n3. item 3"), "ordered_list"
        )

    def test_block_to_block_type_with_paragraph(self):
        self.assertEqual(block_to_block_type("here is some text"), "paragraph")

    def test_block_to_block_type_with_quote(self):
        self.assertEqual(
            block_to_block_type(">here is some text\n>that is quoted"), "quote"
        )

    def test_block_to_block_type_with_incomplete_list(self):
        actual = block_to_block_type(
            "This is the first list item in an attempted list block\n2. This is a list item\n3. This is another list item",
        )
        self.assertEqual(actual, "paragraph")

    def test_block_to_block_type_with_empty_block(self):
        self.assertEqual(block_to_block_type(""), "paragraph")

    def test_markdown_to_html_node(self):
        actual = markdown_to_html_node("# Heading")
        expected = ParentNode("div", [LeafNode("Heading", "h1")])
        self.assertEqual(actual, expected)
        self.assertEqual(actual.to_html(), "<div><h1>Heading</h1></div>")

    def test_markdown_to_html_node_heading_and_list(self):
        markdown = "## Heading\n\n* Item 1\n* Item 2\n* Item 3"
        actual = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div",
            [
                LeafNode("Heading", "h2"),
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode("Item 1")]),
                        ParentNode("li", [LeafNode("Item 2")]),
                        ParentNode("li", [LeafNode("Item 3")]),
                    ],
                ),
            ],
        )
        self.assertEqual(actual, expected)
        self.assertEqual(
            actual.to_html(),
            "<div><h2>Heading</h2><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_markdown_to_html_node_heading_and_paragraphs(self):
        markdown = "# Header 1\n\nThis is a paragraph under header 1.\n\n## Header 2\n\nAnother paragraph, with **bold** text and *italic* text."
        actual = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div",
            [
                LeafNode("Header 1", "h1"),
                ParentNode("p", [LeafNode("This is a paragraph under header 1.")]),
                LeafNode("Header 2", "h2"),
                ParentNode(
                    "p",
                    [
                        LeafNode("Another paragraph, with "),
                        LeafNode("bold", "b"),
                        LeafNode(" text and "),
                        LeafNode("italic", "i"),
                        LeafNode(" text."),
                    ],
                ),
            ],
        )
        self.assertEqual(actual, expected)
        self.assertEqual(
            actual.to_html(),
            "<div><h1>Header 1</h1><p>This is a paragraph under header 1.</p><h2>Header 2</h2><p>Another paragraph, with <b>bold</b> text and <i>italic</i> text.</p></div>",
        )

    def test_markdown_to_html_node_code_block(self):
        markdown = "- Item in an unordered list\n- Another item\n\n1. First item in ordered list\n2. Second item\n\n```code block```"
        actual = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode("Item in an unordered list")]),
                        ParentNode("li", [LeafNode("Another item")]),
                    ],
                ),
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", [LeafNode("First item in ordered list")]),
                        ParentNode("li", [LeafNode("Second item")]),
                    ],
                ),
                ParentNode("pre", [LeafNode("code block", "code")]),
            ],
        )
        self.assertEqual(actual, expected)

        self.assertEqual(
            actual.to_html(),
            "<div><ul><li>Item in an unordered list</li><li>Another item</li></ul><ol><li>First item in ordered list</li><li>Second item</li></ol><pre><code>code block</code></pre></div>",
        )

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(node.to_html())
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
