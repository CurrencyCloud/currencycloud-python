import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *


class TestTransactions:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_transactions_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('transactions/can_find')

            transactions = self.client.transactions.find(currency="GBP", per_page=1)

            assert len(transactions) == 1

            transaction = transactions[0]
            assert transaction is not None

            assert isinstance(transaction, Transaction)
            assert transaction.currency == "GBP"

    def test_transactions_can_retrieve(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('transactions/can_retrieve')

            transaction = self.client.transactions.retrieve("da45e164-620a-47e7-80a6-2e66d5919276")
            assert transaction is not None
            assert transaction.currency == "GBP"
