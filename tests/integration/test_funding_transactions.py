from betamax import Betamax

from currencycloud import Client, Config


class TestFundingTransactions:
	def setup_method(self, method):
		# TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
		# login_id and api_key with valid credentials before running the tests
		login_id = 'development@currencycloud.com'
		api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
		environment = Config.ENV_DEMO

		self.client = Client(login_id, api_key, environment)

	def test_transaction_can_get_funding_transaction(self):
		with Betamax(self.client.config.session) as betamax:
			betamax.use_cassette('funding_transactions/can_get_funding_transaction')
			transaction = self.client.funding_transactions.get_funding_transaction('e68301d3-5b04-4c1d-8f8b-13a9b8437040')

			assert transaction.id is not None
			assert transaction.amount is not None
			assert transaction.currency == "USD"
			assert transaction.sender['sender_country'] == "GB"
