import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *


class TestConversions:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_conversions_can_create(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('conversions/create')

            conversion = self.client.conversions.create(buy_currency="EUR",
                                                        sell_currency="GBP",
                                                        fixed_side="buy",
                                                        amount="1000",
                                                        term_agreement="true")

            assert conversion is not None
            assert isinstance(conversion, Conversion)

            assert conversion.id is not None
            assert conversion.client_buy_amount == "1000.00"

    def test_actions_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('conversions/find')

            conversions = self.client.conversions.find(per_page=1)

            assert conversions
            assert len(conversions) == 1

            conversion = conversions[0]

            assert conversion is not None
            assert isinstance(conversion, Conversion)

            assert conversion.client_buy_amount == "1000.00"

    def test_actions_can_retrieve(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('conversions/retrieve')

            conversion = self.client.conversions.retrieve("a26ffc86-c0f6-45d8-8c1c-6a3e579ce974")

            assert conversion is not None
            assert isinstance(conversion, Conversion)

            assert conversion.id == "a26ffc86-c0f6-45d8-8c1c-6a3e579ce974"
            assert conversion.client_buy_amount == "1000.00"
