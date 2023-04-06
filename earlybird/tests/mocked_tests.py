import os
import unittest
from unittest.mock import patch, MagicMock
from redditAPI import get_access_token
from redditAPI import get_posts


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


class TestGetPosts(unittest.TestCase):

    @patch("redditAPI.requests.get")
    @patch("redditAPI.get_access_token")
    def test_get_posts_access_token_none(self,
                                         mock_get_access_token,
                                         mock_requests_get):
        mock_get_access_token.return_value = None
        result = get_posts("query")
        self.assertIsNone(result)

    @patch("redditAPI.time.sleep")
    @patch("redditAPI.requests.get")
    @patch("redditAPI.get_access_token")
    def test_get_posts_success(self, mock_get_access_token,
                               mock_requests_get,
                               mock_time_sleep):
        mock_get_access_token.return_value = "access_token"

        mock_posts_response = MagicMock(raise_for_status=lambda: None)
        mock_posts_response.json.return_value = {
            "data": {
                "children": [
                    {
                        "data": {
                            "title": "Test title",
                            "permalink": "/r/test/comments/1a2b3c/test_title/"
                        }
                    },
                    {
                        "data": {
                            "title": "Another test title",
                            "permalink": "/r/test/comments/4d5e6f/another_test_title/"
                        }
                    },
                ],
                "after": None
            }
        }

        mock_requests_get.return_value = mock_posts_response

        result = get_posts("query", cap=2)
        self.assertIsNotNone(result)
        self.assertEqual(len(result[0]), 2)
        self.assertIn("Test title", result[0])
        self.assertIn("Another test title", result[0])
        self.assertEqual(len(result[1]), 2)
        self.assertIn("/r/test/comments/1a2b3c/test_title/", result[1])
        self.assertIn("/r/test/comments/4d5e6f/another_test_title/", result[1])

if __name__ == '__main__':
    unittest.main()
