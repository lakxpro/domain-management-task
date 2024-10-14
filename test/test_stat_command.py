import unittest
from unittest.mock import patch, Mock
from click.testing import CliRunner
from file_client import file_client

class TestFileClientCLI(unittest.TestCase):
    
    def setUp(self):
        """Set up the Click test runner."""
        self.runner = CliRunner()
        self.base_url = "http://localhost/"
        self.uuid = "123e4567-e89b-12d3-a456-426614174001"

    @patch('file_client.requests.get')
    def test_stat_command_success(self, mock_get):
        """Test the 'stat' command with a successful response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "example.txt",
            "create_datetime": "2024-10-10T09:39:06",
            "size": 1024,
            "mimetype": "text/plain"
        }
        mock_get.return_value = mock_response
        
        result = self.runner.invoke(file_client, ['--base-url', self.base_url, 'stat', self.uuid])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("File Name: example.txt", result.output)
        self.assertIn("Creation Date: 2024-10-10T09:39:06", result.output)
        self.assertIn("Size: 1024 bytes", result.output)
        self.assertIn("MIME Type: text/plain", result.output)

    @patch('file_client.requests.get')
    def test_stat_command_file_not_found(self, mock_get):
        """Test the 'stat' command when the file is not found (404)."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.runner.invoke(file_client, ['--base-url', self.base_url, 'stat', self.uuid])

        print(result.output)
        if result.exception:
            print(result.exception)
        
        self.assertEqual(result.exit_code, 0)
        self.assertIn("File not found (404)", result.output)


if __name__ == '__main__':
    unittest.main()
