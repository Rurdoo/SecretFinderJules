import unittest
from unittest.mock import patch
import sys
import io

import SecretFinder

class TestSecretFinder(unittest.TestCase):
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_parser_error(self, mock_stdout, mock_exit):
        with patch.object(sys, 'argv', ['SecretFinder.py']):
            msg = "Test error message"
            SecretFinder.parser_error(msg)

            # Verify sys.exit was called with 0
            mock_exit.assert_called_once_with(0)

            # Verify output message
            output = mock_stdout.getvalue()
            self.assertIn('Usage: python SecretFinder.py [OPTIONS] use -h for help', output)
            self.assertIn('Error: Test error message', output)

if __name__ == '__main__':
    unittest.main()
