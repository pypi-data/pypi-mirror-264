import unittest
import requests
from unittest.mock import patch
from structhub import StructHubClient

class TestStructHubClient(unittest.TestCase):
    def setUp(self):
        self.client = StructHubClient(api_key="dummy_api_key")

    @patch('structhub_client.requests.post')
    def test_extract_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = "Extracted text"
        extracted_text = self.client.extract(file_path="test_file.txt")
        self.assertEqual(extracted_text, "Extracted text")

    @patch('structhub_client.requests.post')
    def test_extract_retry(self, mock_post):
        mock_post.return_value.status_code = 429
        mock_post.return_value.raise_for_status.side_effect = [
            None,  # Retry successful
            requests.exceptions.HTTPError("429 Client Error: Too Many Requests")
        ]
        with self.assertRaises(Exception):
            self.client.extract(file_path="test_file.txt", max_retries=1)

    @patch('structhub_client.requests.post')
    def test_extract_failure(self, mock_post):
        mock_post.return_value.status_code = 500
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.extract(file_path="test_file.txt")

if __name__ == '__main__':
    unittest.main()
