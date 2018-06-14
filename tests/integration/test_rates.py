from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import *


class TestRates:

    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

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
