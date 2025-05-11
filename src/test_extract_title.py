import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("# Hello")
        self.assertEqual(title, "Hello")

    def test_extract_title_not_first(self):
        title = extract_title("This is not the title\n\n### This is a small header\n\n# Hello")
        self.assertEqual(title, "Hello")

    def test_extract_title_not_found(self):
        self.assertRaises(Exception, extract_title, "This markdown has no h1 block\n\nThis is not ok")

if __name__ == "__main__":
    unittest.main()