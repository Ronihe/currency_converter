from unittest import TestCase
from flask import session
from app import *


class FlaskTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(Self):
        """Reset the """
        pass

    def test_format_currency(self):
        """ make sure the format_currency(amt, curr) function is working"""

        assert format_currency(10, 'USD') == '$ 10'
        assert format_currency(0.9909, 'USD') == '$ 0.99'
        assert format_currency(100.89, 'JPY') == '￥ 100'

    def test_show_convert_form(self):
        """ make sure show_convert_form has correct route"""

        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<form>', response.data)
            self.assertIn(b'convert_from', response.data)
            self.assertIn(b'convert_to', response.data)
            self.assertIn(b'amount', response.data)
            self.assertIn(b'calculated_list', response.data)

    def test_show_converted_curr(self):
        """ make sure the session works"""

        with self.client:
            response = self.client.post(
                '/calc_nums',
                json={
                    "convert_from": "USD",
                    "convert_to": "EUR",
                    "amount": 1.99
                })
            session['calculated'] = []
            self.assertEqual(response.status_code, 405)
            self.assertIsInstance(session.get('calculated'), list)
