import unittest

from markdown_blocks import markdown_to_blocks


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
