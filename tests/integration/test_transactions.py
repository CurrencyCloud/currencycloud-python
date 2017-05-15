import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *


class TestTransactions:
    def setup_method(self, method):
        login_id = 'api.test.user1@currencycloud.com'
        api_key = '0a14256abc393cdc238672b2d42d54f5581937f3ee23b76d5cfa842f63f8364d'
        environment = Config.ENV_DEMONSTRATION

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
