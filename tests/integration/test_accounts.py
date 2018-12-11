from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import *
from tests.utils import parse
from tests.load_schema import assert_valid_schema


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

            assert_valid_schema(parse.toJSon(account), 'account/can_get_current_schema.json')

    def test_accounts_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/find')

            accounts = self.client.accounts.find(brand="currencycloud", per_page=1)

            assert accounts
            assert len(accounts) == 1

            account = accounts[0]

            assert account is not None
            assert isinstance(account, Account)

            assert account.brand == "currencycloud"

def test_accounts_can_retrieve(self):
    with Betamax(self.client.config.session) as betamax:
        betamax.use_cassette('accounts/retrieve')

        account = self.client.accounts.retrieve("8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8")

        assert account is not None
        assert isinstance(account, Account)

        assert account.id == "8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8"

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
        assert account.city == "Manchester"
