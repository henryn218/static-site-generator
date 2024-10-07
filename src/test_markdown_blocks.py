import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type


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

    def test_block_to_block_type_with_incomplete_list(self):
        actual = block_to_block_type(
            "This is the first list item in an attempted list block\n2. This is a list item\n3. This is another list item",
        )
        self.assertEqual(actual, "paragraph")

    def test_block_to_block_type_with_empty_block(self):
        self.assertEqual(block_to_block_type(""), "paragraph")
