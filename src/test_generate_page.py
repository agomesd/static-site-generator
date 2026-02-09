import unittest
from pathlib import Path
from generate_page import GeneratePage


BASE_DIR = Path(__file__).resolve().parent

from_path = BASE_DIR.parent / "content" / "index.md"
template = BASE_DIR.parent / "template.html"
dest_path = BASE_DIR.parent / "docs" / "index.html"


class TestGeneratePage(unittest.TestCase):
    pass
    # def test_extract_title(self):
    #     page_gen = GeneratePage(from_path, template, dest_path)
    #     page_gen.generate_page()
    #     title = page_gen.extract_title()

    #     self.assertEqual(title, "Tolkien Fan Club")

    #     page_gen = GeneratePage(
    #         """
    # ## No title here
    # """
    #     )
    #     with self.assertRaises(Exception):
    #         page_gen.extract_title()
