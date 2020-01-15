from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import *

class TestFunding:

    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_funding_accounts_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('funding/accounts_find')

            accounts = self.client.funding.find_funding_accounts(currency="GBP", per_page=5)

            assert accounts
            assert len(accounts) == 1

            account = accounts[0]

            assert account is not None
            assert isinstance(account, FundingAccount)

            assert account.id == "b7981972-8e29-485b-8a4a-9643fc6ae3sa"
            assert account.account_id == "8d98bdc8-e8e3-47dc-bd08-3dd0f4f7ea7b"
            assert account.account_number == "012345678"
            assert account.account_number_type == "account_number"
            assert account.account_holder_name == "Jon Doe"
            assert account.bank_name == "Starling"
            assert account.bank_address == "3rd floor, 2 Finsbury Avenue, London, EC2M 2PP, GB"
            assert account.bank_country == "UK"
            assert account.currency == "GBP"
            assert account.payment_type == "regular"
            assert account.regular_routing_code == "010203"
            assert account.regular_routing_code_type == "sort_code"
            assert account.priority_routing_code == ""
            assert account.priority_routing_code_type == ""
            assert account.created_at == "2018-05-14T14:18:30+00:00"
            assert account.updated_at == "2018-05-14T14:19:30+00:00"

