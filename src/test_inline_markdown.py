import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("Here is some **bold** text", TextType.TEXT)]

        actual = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Here is some ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" text", TextType.TEXT, None),
        ]
        self.assertListEqual(actual, expected)

    def test_split_nodes_delimiter_at_end_of_text(self):
        old_nodes = [TextNode("Here is some *italic text*", TextType.TEXT)]

        actual = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("Here is some ", TextType.TEXT, None),
            TextNode("italic text", TextType.ITALIC, None),
        ]
        self.assertListEqual(actual, expected)

    def test_split_nodes_delimiter_with_multiple_old_nodes(self):
        old_nodes = [
            TextNode("Here is some *italic text*", TextType.TEXT),
            TextNode("Here is some **bold** text", TextType.TEXT),
        ]

        actual = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("Here is some ", TextType.TEXT, None),
            TextNode("italic text", TextType.ITALIC, None),
            TextNode("Here is some **bold** text", TextType.TEXT),
        ]
        self.assertListEqual(actual, expected)

    def test_split_nodes_delimiter_with_old_nodes_of_different_types(self):
        old_nodes = [
            TextNode("Here is some italic text", TextType.ITALIC),
            TextNode("Here is some **bold** text", TextType.TEXT),
        ]

        actual = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Here is some italic text", TextType.ITALIC),
            TextNode("Here is some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(actual, expected)

    def test_split_nodes_delimiter_after_old_nodes_processed_for_bold_types(self):
        old_nodes = [
            TextNode("Here is some bold text", TextType.BOLD),
            TextNode("Here is some *italic* text and `code` text", TextType.TEXT),
        ]

        actual = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("Here is some bold text", TextType.BOLD),
            TextNode("Here is some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text and `code` text", TextType.TEXT),
        ]
        self.assertListEqual(actual, expected)

    def test_split_nodes_delimiter_for_code_type(self):
        old_nodes = [
            TextNode("Here is some *italic* text and `code` text", TextType.TEXT),
        ]

        actual = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        expected = [
            TextNode("Here is some *italic* text and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(actual, expected)

    def test_split_nodes_delimiter_for_nonterminating_delimiters(self):
        old_nodes = [
            TextNode("Here is some *italic text and `code` text", TextType.TEXT),
        ]
        actual = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(actual, old_nodes)


class TestInlineMarkdownBootDevCases(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
