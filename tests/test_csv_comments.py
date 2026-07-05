import io
import unittest

from csv_comments import find_comment_column, load_comments_from_csv


class CsvCommentsTest(unittest.TestCase):
    def test_loads_xquik_text_column(self):
        csv_file = io.BytesIO(
            b"createdAt,text,author\n2026-07-05,Great walk-through,ann\n"
        )

        self.assertEqual(load_comments_from_csv(csv_file), ["Great walk-through"])

    def test_filters_blank_comments(self):
        csv_file = io.StringIO("Username,Comment\nann,Useful demo\nbob,   \n")

        self.assertEqual(load_comments_from_csv(csv_file), ["Useful demo"])

    def test_rejects_missing_comment_column(self):
        with self.assertRaisesRegex(ValueError, "Comment, comments, or text"):
            find_comment_column(["Username", "Score"])


if __name__ == "__main__":
    unittest.main()
