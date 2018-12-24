from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import *


class TestAccounts:

    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_accounts_can_get_current(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/can_get_current')
            account = self.client.accounts.current()

            assert isinstance(account, Account)

            assert account is not None
            assert account.id is not None
            assert account.account_name is not None
            assert account.brand == "currencycloud"
            assert account.your_reference is None
            assert account.status is not None
            assert account.street is not None
            assert account.city is not None
            assert account.state_or_province is None
            assert account.country is not None
            assert account.postal_code is not None
            assert account.spread_table is not None
            assert account.legal_entity_type is not None
            assert account.created_at is not None
            assert account.updated_at is not None
            assert account.identification_type is not None
            assert account.identification_value is not None
            assert account.short_reference is not None
            assert account.api_trading is not None
            assert account.online_trading is not None
            assert account.phone_trading is not None
            assert account.process_third_party_funds is not None
            assert account.settlement_type is not None

    def test_accounts_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/find')

            accounts = self.client.accounts.find(brand="currencycloud", per_page=1)

            assert accounts
            assert len(accounts) == 1

            account = accounts[0]

            assert account is not None
            assert isinstance(account, Account)

            assert account.id is not None
            assert account.account_name is not None
            assert account.brand == "currencycloud"
            assert account.your_reference is None
            assert account.status is not None
            assert account.street is None
            assert account.city is None
            assert account.state_or_province is None
            assert account.country is None
            assert account.postal_code is None
            assert account.spread_table is not None
            assert account.legal_entity_type is None
            assert account.created_at is None
            assert account.updated_at is None
            assert account.identification_type is None
            assert account.identification_value is None
            assert account.short_reference is not None
            assert account.api_trading is not None
            assert account.online_trading is not None
            assert account.phone_trading is not None
            assert account.process_third_party_funds is not None
            assert account.settlement_type is not None

    def test_accounts_can_retrieve(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/retrieve')

            account = self.client.accounts.retrieve("8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8")

            assert account is not None
            assert isinstance(account, Account)

            assert account.id == "8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8"
            assert account.account_name is not None
            assert account.brand == "currencycloud"
            assert account.your_reference == ''
            assert account.status is not None
            assert account.street is None
            assert account.city is None
            assert account.state_or_province is None
            assert account.country is None
            assert account.postal_code is None
            assert account.spread_table == 'fxcg_rfx_default'
            assert account.legal_entity_type is None
            assert account.created_at is not None
            assert account.updated_at is not None
            assert account.identification_type is None
            assert account.identification_value is None
            assert account.short_reference is not None
            assert account.api_trading is not None
            assert account.online_trading is not None
            assert account.phone_trading is not None
            assert account.process_third_party_funds is not None
            assert account.settlement_type is not None

    def test_accounts_can_create(self):
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
            assert account.brand == "currencycloud"
            assert account.your_reference is None
            assert account.status is not None
            assert account.street is None
            assert account.city is None
            assert account.state_or_province is None
            assert account.country == 'GB'
            assert account.postal_code is None
            assert account.spread_table == 'no_markup'
            assert account.legal_entity_type == 'company'
            assert account.created_at is not None
            assert account.updated_at is not None
            assert account.identification_type is None
            assert account.identification_value is None
            assert account.short_reference is not None
            assert account.api_trading is not None
            assert account.online_trading is not None
            assert account.phone_trading is not None
            assert account.process_third_party_funds is not None
            assert account.settlement_type is not None

    def test_accounts_can_update(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/update')

            account = self.client.accounts.retrieve("8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8")
            assert account is not None

            account.city = "Manchester"
            account.update()
            assert account.city == "Manchester"

            account = self.client.accounts.retrieve("8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8")
            assert account is not None

            assert account.id == '8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8'
            assert account.account_name == "Currency Cloud"
            assert account.brand == "currencycloud"
            assert account.your_reference == ''
            assert account.status is not None
            assert account.street is None
            assert account.city == "Manchester"
            assert account.state_or_province is None
            assert account.country is None
            assert account.postal_code is None
            assert account.spread_table == 'fxcg_rfx_default'
            assert account.legal_entity_type is None
            assert account.created_at is not None
            assert account.updated_at is not None
            assert account.identification_type is None
            assert account.identification_value is None
            assert account.short_reference is not None
            assert account.api_trading is not None
            assert account.online_trading is not None
            assert account.phone_trading is not None
            assert account.process_third_party_funds is not None
            assert account.settlement_type is not None
