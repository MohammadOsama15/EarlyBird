import os
import requests
import json
import unittest
from unittest.mock import patch, MagicMock
from redditAPI import get_access_token


class TestGetAccessToken(unittest.TestCase):

    def setUp(self):
        self.environ_patcher = patch.dict(
            os.environ,
            {
                'CLIENT_ID': 'test_client_id',
                'SECRET_KEY': 'test_secret_key',
                'username': 'test_username',
                'password': 'test_password'
            }
        )
        self.environ_patcher.start()

    def tearDown(self):
        self.environ_patcher.stop()

    @patch('requests.post')
    def test_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'access_token': 'test_access_token'}
        mock_post.return_value = mock_response

        access_token = get_access_token()
        expected = 'bearer test_access_token'

        self.assertEqual(access_token, expected)
        mock_post.assert_called_once()
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()

if __name__ == '__main__':
    unittest.main()
