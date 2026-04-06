import unittest
import subprocess
import os
import sys

class TestSecretFinder(unittest.TestCase):

    def setUp(self):
        self.test_file_name = "dummy_test.js"
        # SecretFinder uses a base of rules. Let's create a JS file with some of them.
        self.js_content = """
        var api_key = 'AIzaSyAXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXa';
        var aws_access = 'AKIAIOSFODNN7EXAMPLE';
        var something_else = 'just a normal string';
        """
        with open(self.test_file_name, "w") as f:
            f.write(self.js_content)

    def tearDown(self):
        if os.path.exists(self.test_file_name):
            os.remove(self.test_file_name)

    def test_cli_output(self):
        # Run SecretFinder.py as a subprocess
        result = subprocess.run(
            [sys.executable, "SecretFinder.py", "-i", self.test_file_name, "-o", "cli"],
            capture_output=True,
            text=True
        )

        # Output should be something like:
        # [ + ] URL: file://.../dummy_test.js
        # google_api	->	AIzaSyAXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXa
        # amazon_aws_access_key_id	->	AKIAIOSFODNN7EXAMPLE

        output = result.stdout

        # Verify no errors in stderr
        self.assertEqual(result.stderr, "")

        # Verify the findings
        self.assertIn("google_api", output)
        self.assertIn("AIzaSyAXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXa", output)

        self.assertIn("amazon_aws_access_key_id", output)
        self.assertIn("AKIAIOSFODNN7EXAMPLE", output)

if __name__ == '__main__':
    unittest.main()
