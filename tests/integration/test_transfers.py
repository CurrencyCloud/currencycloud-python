import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *


class TestTransfers:
    def setup_method(self, method):
        login_id = 'api.test.user1@currencycloud.com'
        api_key = '0a14256abc393cdc238672b2d42d54f5581937f3ee23b76d5cfa842f63f8364d'
        environment = Config.ENV_DEMONSTRATION

        self.client = Client(login_id, api_key, environment)

    def test_transfers_can_create(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('transfers/create')

            transfer = self.client.transfers.create(source_account_id="d0ad035e-b699-4fcd-a73c-13fb0910a884",
                                                    destination_account_id="e54a5e86-80ad-4434-90fe-0c8c751666de",
                                                    currency="GBP",
                                                    amount="1000")

            assert transfer is not None

            assert isinstance(transfer, Transfer)
            assert transfer.currency == "GBP"

    def test_transfers_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('transfers/can_find')

            transfers = self.client.transfers.find(currency="GBP", per_page=1)

            assert len(transfers) == 1

            transfer = transfers[0]
            assert transfer is not None

            assert isinstance(transfer, Transfer)
            assert transfer.currency == "GBP"

    def test_transfers_can_retrieve(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('transfers/can_retrieve')

            transfer = self.client.transfers.retrieve("f4bf00d7-1672-463d-96b0-9e9643793978")
            assert transfer is not None
            assert transfer.currency == "GBP"
