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
            assert account is not None

            assert account.id == "8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8"
            assert account.account_name == "Currency Cloud"

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

    def test_accounts_can_find_post(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/find_post')

            accounts = self.client.accounts.find_post(brand="currencycloud", per_page=1)

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

    def test_accounts_can_get_payment_charges_setting(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/can_get_payment_charges_setting')

            settings = self.client.accounts.retrieve_payment_charges_settings('e277c9f9-679f-454f-8367-274b3ff977ff')

            assert settings is not None
            assert isinstance(settings[0], PaymentChargesSettings)
            assert settings[0].charge_settings_id == "18f3f814-fef0-4211-a028-fe22c4b69818"
            assert settings[1].charge_settings_id == "734bd817-0ab0-49ae-9e96-1f623a809f11"

    def test_accounts_can_manage_payment_charges_setting(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('accounts/can_manage_payment_charges_setting')

            settings = self.client.accounts.payment_charges_settings('e277c9f9-679f-454f-8367-274b3ff977ff',
                                                                     '18f3f814-fef0-4211-a028-fe22c4b69818',
                                                                     enabled='true',
                                                                     default='true')
            assert settings is not None
            assert isinstance(settings, PaymentChargesSettings)
            assert settings.charge_settings_id == "18f3f814-fef0-4211-a028-fe22c4b69818"
            assert settings.account_id == "e277c9f9-679f-454f-8367-274b3ff977ff"
            assert settings.charge_type == "ours"
            assert settings.enabled is True
            assert settings.default is True
