from betamax import Betamax

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
            assert transaction.id is not None
            assert transaction.balance_id is not None
            assert transaction.account_id is not None
            assert transaction.currency == "GBP"
            assert transaction.amount is not None
            assert transaction.balance_amount is None
            assert transaction.type is not None
            assert transaction.related_entity_type is not None
            assert transaction.related_entity_id is not None
            assert transaction.related_entity_short_reference == '20170515-QHBCNR'
            assert transaction.status is not None
            assert transaction.reason == ''
            assert transaction.settles_at is not None
            assert transaction.created_at is not None
            assert transaction.updated_at is not None
            assert transaction.completed_at is not None
            assert transaction.action is not None

    def test_transactions_can_retrieve(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('transactions/can_retrieve')

            transaction = self.client.transactions.retrieve("da45e164-620a-47e7-80a6-2e66d5919276")
            assert isinstance(transaction, Transaction)
            assert transaction is not None

            assert transaction.id == 'da45e164-620a-47e7-80a6-2e66d5919276'
            assert transaction.balance_id is not None
            assert transaction.account_id is not None
            assert transaction.currency == "GBP"
            assert transaction.amount is not None
            assert transaction.balance_amount is None
            assert transaction.type is not None
            assert transaction.related_entity_type is not None
            assert transaction.related_entity_id is not None
            assert transaction.related_entity_short_reference == '20170515-QHBCNR'
            assert transaction.status is not None
            assert transaction.reason == ''
            assert transaction.settles_at is not None
            assert transaction.created_at is not None
            assert transaction.updated_at is not None
            assert transaction.completed_at is not None
            assert transaction.action is not None
