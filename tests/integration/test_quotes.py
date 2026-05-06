from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import *


class TestQuotes:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_quotes_can_create(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('quotes/create')

            quote = self.client.quotes.create(buy_currency="USD",
                                              sell_currency="EUR",
                                              fixed_side="sell",
                                              amount="100",
                                              hold_period="30s")

            assert quote is not None
            assert isinstance(quote, Quote)

            assert quote.quote_id is not None
            assert quote.buy_currency == "USD"
            assert quote.sell_currency == "EUR"
            assert quote.fixed_side == "sell"
            assert quote.client_sell_amount == "100.0"
