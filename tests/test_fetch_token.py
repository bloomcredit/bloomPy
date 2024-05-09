import unittest
from bloom.bloom import fetch_auth_token


class TestFetchAuthToken(unittest.TestCase):

    def test_empty_env(self):
        self.assertIsNone(fetch_auth_token(audience="", client_id="", client_secret="", grant_type=""))
