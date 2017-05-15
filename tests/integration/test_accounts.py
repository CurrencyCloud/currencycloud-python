import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *


class TestAccounts:
    def setup_method(self, method):
        login_id = 'rjnienaber@gmail.com'
        api_key = 'ef0fd50fca1fb14c1fab3a8436b9ecb65f02f129fd87eafa45ded8ae257528f0'
        environment = Config.ENV_DEMONSTRATION

        self.client = Client(login_id, api_key, environment)

    def test_accounts_can_get_current(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/can_get_current')

            account = self.client.accounts.current()
            assert account is not None

            assert account.id == "8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8"
            assert account.account_name == "Currency Cloud"

    def test_actions_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/find')

            accounts = self.client.accounts.find(brand="currencycloud", per_page=1)

            assert accounts
            assert len(accounts) == 1

            account = accounts[0]

            assert account is not None
            assert isinstance(account, Account)

            assert account.brand == "currencycloud"

    def test_actions_can_retrieve(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/retrieve')

            account = self.client.accounts.retrieve("8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8")

            assert account is not None
            assert isinstance(account, Account)

            assert account.id == "8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8"

    def test_actions_can_create(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/create')

            account = self.client.accounts.create(account_name="Currency Cloud Testing Environment",
                                                  country="GB",
                                                  brand="currencycloud",
                                                  spread_table="no_markup",
                                                  legal_entity_type="company")

            assert account is not None
            assert isinstance(account, Account)

            assert account.id is not None
            assert account.account_name == "Currency Cloud Testing Environment"

    def test_actions_can_update(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/update')

            account = self.client.accounts.retrieve("8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8")
            assert account is not None

            account.city = "Manchester"
            account.update()
            assert account.city == "Manchester"

            account = self.client.accounts.retrieve("8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8")
            assert account is not None
            assert account.city == "Manchester"
