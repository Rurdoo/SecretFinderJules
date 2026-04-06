import unittest
import sys
import os

# Add parent directory to path so we can import SecretFinder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from SecretFinder import getContext

class TestGetContext(unittest.TestCase):
    def test_single_match(self):
        content = "Some prefix text AIzaSyA-0123456789012345678901234567890 and some suffix text."
        matches = [('AIzaSyA-0123456789012345678901234567890', 17, 56)]
        name = "google_api"
        result = getContext(matches, content, name)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['matched'], 'AIzaSyA-0123456789012345678901234567890')
        self.assertEqual(result[0]['name'], 'google_api')
        self.assertEqual(len(result[0]['context']), 1)
        self.assertFalse(result[0]['multi_context'])

    def test_multiple_matches_same_string(self):
        content = "First AIzaSyA-0123456789012345678901234567890 middle AIzaSyA-0123456789012345678901234567890 last"
        matches = [
            ('AIzaSyA-0123456789012345678901234567890', 6, 45),
            ('AIzaSyA-0123456789012345678901234567890', 53, 92)
        ]
        name = "google_api"
        result = getContext(matches, content, name)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['matched'], 'AIzaSyA-0123456789012345678901234567890')
        self.assertEqual(result[0]['name'], 'google_api')
        self.assertEqual(len(result[0]['context']), 2)
        self.assertTrue(result[0]['multi_context'])

    def test_multiple_different_matches(self):
        content = "API1 AIzaSyA-0123456789012345678901234567890 and API2 AIzaSyB-0123456789012345678901234567890"
        matches = [
            ('AIzaSyA-0123456789012345678901234567890', 5, 44),
            ('AIzaSyB-0123456789012345678901234567890', 54, 93)
        ]
        name = "google_api"
        result = getContext(matches, content, name)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['matched'], 'AIzaSyA-0123456789012345678901234567890')
        self.assertEqual(result[1]['matched'], 'AIzaSyB-0123456789012345678901234567890')
        self.assertFalse(result[0]['multi_context'])
        self.assertFalse(result[1]['multi_context'])

    def test_empty_matches(self):
        content = "No API keys here"
        matches = []
        name = "google_api"
        result = getContext(matches, content, name)
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
