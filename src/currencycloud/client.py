'''This module provides a the Client interface to the CC APIs'''

from currencycloud.clients import *
from contextlib import contextmanager

from currencycloud.config import Config
from currencycloud.http import Http


class Client(Http):
    '''The Client interfacing to the CC APIs'''

    _accounts_client = None
    _auth_client = None
    _balances_client = None
    _beneficiaries_client = None
    _contacts_client = None
    _conversions_client = None
    _payers_client = None
    _payments_client = None
    _rates_client = None
    _reference_client = None
    _settlements_client = None
    _transactions_client = None
    _transfers_client = None

    def __init__(self, login_id, api_key, environment='demo'):
        config = Config(login_id, api_key, environment)

        super(Client, self).__init__(config)

    @classmethod
    def with_config(cls, config):
        '''Instantiate a new Client using a config instance'''
        return cls(config.login_id, config.api_key, config.environment)

    def authenticate(self):
        '''Generate an auth token an store it in the config.'''
        response = self.auth.authenticate()
        self.config.auth_token = response['auth_token']

    def close_session(self):
        '''Terminate the Auth Token validity'''
        self.auth.close_session()
        self.config.auth_token = None
        return True

    @contextmanager
    def on_behalf_of(self, uuid):
        '''Yields a new client object with an on_behalf_of setting.'''

        # Use a new client, without changing the `self` configuration to stay thread-safe.

        clone = Client.with_config(self.config)
        clone.config.auth_token = self.config._auth_token
        clone.config.on_behalf_of = uuid

        yield clone

    @property
    def accounts(self):
        '''Get the Accounts client.'''
        if self._accounts_client is None:
            self._accounts_client = Accounts(self.config)
        return self._accounts_client

    @property
    def auth(self):
        '''Get the Authentication client.'''
        if self._auth_client is None:
            self._auth_client = Auth(self.config)
        return self._auth_client

    @property
    def balances(self):
        '''Get the Balances client.'''
        if self._balances_client is None:
            self._balances_client = Balances(self.config)
        return self._balances_client

    @property
    def beneficiaries(self):
        '''Get the Beneficiaries client.'''
        if self._beneficiaries_client is None:
            self._beneficiaries_client = Beneficiaries(self.config)
        return self._beneficiaries_client

    @property
    def contacts(self):
        '''Get the Contacts client.'''
        if self._contacts_client is None:
            self._contacts_client = Contacts(self.config)
        return self._contacts_client

    @property
    def conversions(self):
        '''Get the Conversions client.'''
        if self._conversions_client is None:
            self._conversions_client = Conversions(self.config)
        return self._conversions_client

    @property
    def payers(self):
        '''Get the Payers client.'''
        if self._payers_client is None:
            self._payers_client = Payers(self.config)
        return self._payers_client

    @property
    def payments(self):
        '''Get the Payments client.'''
        if self._payments_client is None:
            self._payments_client = Payments(self.config)
        return self._payments_client

    @property
    def rates(self):
        '''Get the Rates client.'''
        if self._rates_client is None:
            self._rates_client = Rates(self.config)
        return self._rates_client

    @property
    def reference(self):
        '''Get the Reference client.'''
        if self._reference_client is None:
            self._reference_client = Reference(self.config)
        return self._reference_client

    @property
    def settlements(self):
        '''Get the Settlements client.'''
        if self._settlements_client is None:
            self._settlements_client = Settlements(self.config)
        return self._settlements_client

    @property
    def transactions(self):
        '''Get the Transactions client.'''
        if self._transactions_client is None:
            self._transactions_client = Transactions(self.config)
        return self._transactions_client

    @property
    def transfers(self):
        '''Get the Transfers client.'''
        if self._transfers_client is None:
            self._transfers_client = Transfers(self.config)
        return self._transfers_client
