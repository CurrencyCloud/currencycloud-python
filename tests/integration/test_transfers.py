from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import *


class TestTransfers:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_transfers_can_create(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('transfers/can_create')

            transfer = self.client.transfers.create(source_account_id="d0ad035e-b699-4fcd-a73c-13fb0910a884",
                                                    destination_account_id="e54a5e86-80ad-4434-90fe-0c8c751666de",
                                                    currency="GBP",
                                                    amount="1000")

            assert transfer is not None

            assert isinstance(transfer, Transfer)
            assert transfer.id is not None
            assert transfer.short_reference is not None
            assert transfer.source_account_id == 'd0ad035e-b699-4fcd-a73c-13fb0910a884'
            assert transfer.destination_account_id == 'e54a5e86-80ad-4434-90fe-0c8c751666de'
            assert transfer.currency == "GBP"
            assert transfer.amount == '1000.00'
            assert transfer.status is not None
            assert transfer.reason is None
            assert transfer.created_at is not None
            assert transfer.updated_at is not None
            assert transfer.completed_at is not None
            assert transfer.creator_account_id is not None
            assert transfer.creator_contact_id is not None

    def test_transfers_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('transfers/can_find')

            transfers = self.client.transfers.find(currency="GBP", per_page=1)

            assert len(transfers) == 1

            transfer = transfers[0]
            assert transfer is not None

            assert isinstance(transfer, Transfer)
            assert transfer.id is not None
            assert transfer.short_reference is not None
            assert transfer.source_account_id == 'd0ad035e-b699-4fcd-a73c-13fb0910a884'
            assert transfer.destination_account_id == 'e54a5e86-80ad-4434-90fe-0c8c751666de'
            assert transfer.currency == "GBP"
            assert transfer.amount == '1000.00'
            assert transfer.status is not None
            assert transfer.reason == ''
            assert transfer.created_at is not None
            assert transfer.updated_at is not None
            assert transfer.completed_at is not None
            assert transfer.creator_account_id is not None
            assert transfer.creator_contact_id is not None

    def test_transfers_can_retrieve(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('transfers/can_retrieve')

            transfer = self.client.transfers.retrieve("f4bf00d7-1672-463d-96b0-9e9643793978")
            assert transfer is not None
            assert transfer.id == 'f4bf00d7-1672-463d-96b0-9e9643793978'
            assert transfer.short_reference is not None
            assert transfer.source_account_id == 'd0ad035e-b699-4fcd-a73c-13fb0910a884'
            assert transfer.destination_account_id == 'e54a5e86-80ad-4434-90fe-0c8c751666de'
            assert transfer.currency == "GBP"
            assert transfer.amount == '1000.00'
            assert transfer.status is not None
            assert transfer.reason == ''
            assert transfer.created_at is not None
            assert transfer.updated_at is not None
            assert transfer.completed_at is not None
            assert transfer.creator_account_id is not None
            assert transfer.creator_contact_id is not None
