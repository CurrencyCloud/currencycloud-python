import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *


class TestRates:

    def setup_method(self, method):
        login_id = 'rjnienaber@gmail.com'
        api_key = 'ef0fd50fca1fb14c1fab3a8436b9ecb65f02f129fd87eafa45ded8ae257528f0'
        environment = Config.ENV_DEMONSTRATION

        self.client = Client(login_id, api_key, environment)

    def test_rates_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('rates/can_find')

            rates = self.client.rates.find(currency_pair="GBPUSD,EURGBP")

            assert rates is not None
            assert rates.currencies
            assert len(rates.unavailable) == 0

            currencies = rates.currencies

            assert len(currencies) == 2

            currency_pairs = []
            for currency in currencies:
                assert currency is not None
                assert isinstance(currency, Rate)

                currency_pairs.append(currency.currency_pair)

            assert 'EURGBP' in currency_pairs

            rate = currencies[0]

            assert rate.bid
            assert rate.offer

    def test_rates_can_provide_detailed_rate(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('rates/can_provide_detailed_rate')

            detailed_rate = self.client.rates.detailed(
                buy_currency="GBP",
                sell_currency="USD",
                fixed_side='buy',
                amount=10000
            )

            assert isinstance(detailed_rate, Rate)
            assert isinstance(float(detailed_rate.client_sell_amount), float)
