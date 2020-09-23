from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import *


class TestWithdrawalAccounts:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_can_find_withdrawal_account(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('withdrawal_accounts/can_find_withdrawal_account')

            accounts = self.client.withdrawal_accounts.find(
                account_id="72970a7c-7921-431c-b95f-3438724ba16f"
            )

            assert accounts
            assert len(accounts) == 1

            account = accounts[0]

            assert account is not None
            assert isinstance(account, WithdrawalAccount)