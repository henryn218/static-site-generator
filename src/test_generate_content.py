import unittest

from generate_content import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        markdown = "# Header 1\n\nParagraph of text"
        self.assertEqual(extract_title(markdown), "Header 1")

    def test_extract_title_missing_title(self):
        markdown = "Text with no title\ntext with no title"
        with self.assertRaises(ValueError, msg="No title line found"):
            extract_title(markdown)
