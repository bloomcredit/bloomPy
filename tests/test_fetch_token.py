import unittest
from src.bloom.bloom import fetch_auth_token

class TestFetchAuthToken(unittest.TestCase):

    def test_empty_env(self):
        """Given empty credentials, the token should return None"""
        self.assertIsNone(
            fetch_auth_token(
                audience="",
                client_id="",
                client_secret="",
                grant_type=""
            )
        )
