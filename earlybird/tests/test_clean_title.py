import unittest
from ..api import clean_title


class TestCleanTitle(unittest.TestCase):

    def test_remove_non_letter_characters(self):
        title = "Hello, World!123"
        expected = "Hello World"
        self.assertEqual(clean_title(title), expected)

    def test_remove_extra_whitespaces(self):
        title = "  Hello   World  "
        expected = "Hello World"
        self.assertEqual(clean_title(title), expected)

    def test_remove_non_letter_characters_and_extra_whitespaces(self):
        title = "  Hello,   World!123  "
        expected = "Hello World"
        self.assertEqual(clean_title(title), expected)

    def test_empty_string(self):
        title = ""
        expected = ""
        self.assertEqual(clean_title(title), expected)

    def test_whitespace_only_string(self):
        title = "     "
        expected = ""
        self.assertEqual(clean_title(title), expected)


if __name__ == '__main__':
    unittest.main()
