import unittest
import json
from src.bloom.bloom import tokenize_json, coalesce


class TestUtilitiies(unittest.TestCase):

    def test_empty_env(self):
        """make sure the more complex replacements take place."""

        consumer_info = {
            "ssn": "123456789",
            "city": "Scranton",
            "line1": "1725 Slough Avenue",
            "state_code": "PA",
            "zipcode": "18503",
            "date_of_birth": "1964-03-15",
            "first_name": "Michael",
            "last_name": "Scott",
            "address_primary": True
        }

        new = tokenize_json('consumer.json', consumer_info)
        data = json.loads(new)
        self.assertTrue(data['data']['attributes']['addresses'][0]['primary'])

    def test_empty_order_portfolio(self):
        """make sure the more complex replacements take place."""

        payload = tokenize_json('order.json', {
            'consumer_id': None,
            'portfolio_id': None,
            'sku': None
        })
        data = json.loads(payload)
        self.assertIs("", data['data']['attributes']['portfolio_id'])

    def test_coalesce(self):

        self.assertIs("", coalesce('', 'hi'))
        self.assertIs("", coalesce('', None, 'hi'))
        self.assertIs("", coalesce(None, '', None, 'hi'))
        self.assertIs("hi", coalesce('hi', None, '', None, 'hi'))

