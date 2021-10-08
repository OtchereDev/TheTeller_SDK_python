from theteller_api_sdk.checkout.checkout import Checkout
import unittest
from theteller_api_sdk.core.core import Client
from theteller_api_sdk.core.environment import Environment
from os import environ

class TestCheckout(unittest.TestCase):
    def setUp(self) -> None:
        env= Environment("test")
        client = Client(merchant_id=environ.get("MERCHANT_ID"),
                    api_key=environ.get("API_KEY"),
                    apiuser=environ.get("API_USERNAME"),
                    environment=env)
        self.checkout = Checkout(client)
    
    def test_checkout_creation(self):
        checkout = self.checkout.createCheckout("test checkout",10,"https://localhost:8000","oliverotchere4@gmail.com")
        self.assertIsNotNone(checkout.get("checkout_url"))
        