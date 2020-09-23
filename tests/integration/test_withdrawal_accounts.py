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

            withdrawal_accounts = self.client.withdrawal_accounts.find(
                account_id="72970a7c-7921-431c-b95f-3438724ba16f"
            )

            assert withdrawal_accounts
            assert len(withdrawal_accounts) == 1

            assert withdrawal_accounts.pagination.total_entries == 1
            assert withdrawal_accounts.pagination.total_pages == 1
            assert withdrawal_accounts.pagination.current_page == 1
            assert withdrawal_accounts.pagination.per_page == 25
            assert withdrawal_accounts.pagination.previous_page == -1
            assert withdrawal_accounts.pagination.next_page == -1
            assert withdrawal_accounts.pagination.order == "created_at"
            assert withdrawal_accounts.pagination.order_asc_desc == "asc"

            withdrawal_account = withdrawal_accounts[0]
            assert withdrawal_account is not None
            assert isinstance(withdrawal_account, WithdrawalAccount)
            assert withdrawal_account.id == "0886ac00-6ab6-41a6-b0e1-8d3faf2e0de2"
            assert withdrawal_account.account_name == "currencycloud"
            assert withdrawal_account.account_holder_name == "The Currency Cloud"
            assert withdrawal_account.account_holder_dob is None
            assert withdrawal_account.routing_code == "123456789"
            assert withdrawal_account.account_number == "01234567890"
            assert withdrawal_account.currency == "USD"
            assert withdrawal_account.account_id == "72970a7c-7921-431c-b95f-3438724ba16f"

    def test_can_find_withdrawal_account2(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('withdrawal_accounts/can_find_withdrawal_account2')

            withdrawal_accounts = self.client.withdrawal_accounts.find()

            assert withdrawal_accounts
            assert len(withdrawal_accounts) == 2

            assert withdrawal_accounts.pagination.total_entries == 2
            assert withdrawal_accounts.pagination.total_pages == 1
            assert withdrawal_accounts.pagination.current_page == 1
            assert withdrawal_accounts.pagination.per_page == 25
            assert withdrawal_accounts.pagination.previous_page == -1
            assert withdrawal_accounts.pagination.next_page == -1
            assert withdrawal_accounts.pagination.order == "created_at"
            assert withdrawal_accounts.pagination.order_asc_desc == "asc"

            withdrawal_account = withdrawal_accounts[0]
            assert withdrawal_account is not None
            assert isinstance(withdrawal_account, WithdrawalAccount)
            assert withdrawal_account.id == "0886ac00-6ab6-41a6-b0e1-8d3faf2e0de2"
            assert withdrawal_account.account_name == "currencycloud"
            assert withdrawal_account.account_holder_name == "The Currency Cloud"
            assert withdrawal_account.account_holder_dob is None
            assert withdrawal_account.routing_code == "123456789"
            assert withdrawal_account.account_number == "01234567890"
            assert withdrawal_account.currency == "USD"
            assert withdrawal_account.account_id == "72970a7c-7921-431c-b95f-3438724ba16f"

            withdrawal_account = withdrawal_accounts[1]
            assert withdrawal_account is not None
            assert isinstance(withdrawal_account, WithdrawalAccount)
            assert withdrawal_account.id == "0886ac00-6ab6-41a6-b0e1-8d3faf2e0de3"
            assert withdrawal_account.account_name == "currencycloud2"
            assert withdrawal_account.account_holder_name == "The Currency Cloud 2"
            assert withdrawal_account.account_holder_dob == "1990-07-20"
            assert withdrawal_account.routing_code == "223456789"
            assert withdrawal_account.account_number == "01234567892"
            assert withdrawal_account.currency == "GBP"
            assert withdrawal_account.account_id == "72970a7c-7921-431c-b95f-3438724ba16e"

    def test_can_pull_funds(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('withdrawal_accounts/can_pull_funds')

            withdrawal_account_funds = self.client.withdrawal_accounts.pull_funds(
                "0886ac00-6ab6-41a6-b0e1-8d3faf2e0de2",
                reference="PullFunds1",
                amount=100.0
            )

            assert withdrawal_account_funds is not None
            assert isinstance(withdrawal_account_funds, WithdrawalAccountFunds)

            assert withdrawal_account_funds.id == "e2e6b7aa-c9e8-4625-96a6-b97d4baab758"
            assert withdrawal_account_funds.withdrawal_account_id == "0886ac00-6ab6-41a6-b0e1-8d3faf2e0de2"
            assert withdrawal_account_funds.reference == "PullFunds1"
            assert withdrawal_account_funds.amount == "100.00"
            assert withdrawal_account_funds.created_at == "2020-06-29T08:02:31+00:00"
