from betamax import Betamax

from currencycloud import Client, Config


class TestCollectionsScreening:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_screening_valid_transaction(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('collections_screening/collections_screening_valid_transaction')

            collections_screening_var = self.client.collections_screening.complete("4159653e-b0e3-449f-93d0-1f25a5dd988b")
            assert collections_screening_var is not None
            assert collections_screening_var.transaction_id is not None


