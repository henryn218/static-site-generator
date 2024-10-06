import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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

    def test_split_nodes_delimiter_for_italic_with_bold(self):
        old_nodes = [
            TextNode(
                "Here is some *italic* text and **bold** and **more bold** text and *more italic text*",
                TextType.TEXT,
            ),
        ]
        actual = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("Here is some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text and **bold** and **more bold** text and ", TextType.TEXT),
            TextNode("more italic text", TextType.ITALIC),
        ]
        self.assertEqual(actual, expected)


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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(actual, expected)

    def test_extract_markdown_images_with_no_images(self):
        text = "This is text with no images"
        actual = extract_markdown_images(text)
        self.assertEqual(actual, [])

    def test_extract_markdown_images_with_malformed_markdown(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg"
        actual = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(actual, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(actual, expected)

    def test_extract_markdown_images_with_no_links(self):
        text = "This is text with no links"
        actual = extract_markdown_links(text)
        self.assertEqual(actual, [])

    def test_extract_markdown_links_with_malformed_markdown(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube]https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(actual, expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        actual = split_nodes_link([node])
        self.assertEqual(actual, expected)

    def test_split_nodes_link_with_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        actual = split_nodes_link([node])
        self.assertEqual(actual, [node])

    def test_split_nodes_link_with_link_and_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        expected = [
            TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link ",
                TextType.TEXT,
            ),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        actual = split_nodes_link([node])
        self.assertEqual(actual, expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        actual = split_nodes_image([node])
        self.assertEqual(actual, expected)

    def test_split_nodes_link_with_image(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        actual = split_nodes_image([node])
        self.assertEqual(actual, [node])

    def test_split_nodes_image_with_image_and_link(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        expected = [
            TextNode(
                "This is text with a ",
                TextType.TEXT,
            ),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(
                " and a link [to boot dev](https://www.boot.dev)",
                TextType.TEXT,
            ),
        ]
        actual = split_nodes_image([node])
        self.assertEqual(actual, expected)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_with_only_image_and_link(self):
        text = "An ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_with_only_italic(self):
        text = "This is text with an *italic* word"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_with_no_markdown(self):
        text = "This is text"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("This is text", TextType.TEXT),
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_with_empty_string(self):
        text = ""
        actual = text_to_textnodes(text)
        expected = []
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_with_consecutive_formatting(self):
        text = "**Bold****Still Bold**"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode("Still Bold", TextType.BOLD),
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_with_format_delimiters_inside_formats(self):
        text = "`code with ** inside`"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("code with ** inside", TextType.CODE),
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_with_empty_image_text(self):
        text = "![](https://example.com/image.jpg)"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.IMAGE, "https://example.com/image.jpg"),
        ]
        self.assertEqual(actual, expected)

    def test_text_to_textnodes_with_empty_format_delimiters(self):
        text = "**"
        actual = text_to_textnodes(text)
        print("\nhi ", actual)
        expected = []
        # self.assertEqual(actual, expected)
