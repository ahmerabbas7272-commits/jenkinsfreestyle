from pathlib import Path
import unittest

PROJECT_DIR = Path(__file__).resolve().parent.parent


class WebAppTests(unittest.TestCase):

    def test_html_file_exists(self):
        self.assertTrue((PROJECT_DIR / "index.html").is_file())

    def test_css_file_exists(self):
        self.assertTrue((PROJECT_DIR / "style.css").is_file())

    def test_page_title(self):
        html = (PROJECT_DIR / "index.html").read_text()
        self.assertIn("My First CI/CD App", html)

    def test_welcome_message(self):
        html = (PROJECT_DIR / "index.html").read_text()
        self.assertIn("Welcome to My First CI/CD App!", html)


if __name__ == "__main__":
    unittest.main()
