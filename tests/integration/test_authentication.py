from betamax import Betamax

from currencycloud import Client, Config


class TestAuthentication:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_authentication_happens_lazily(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('authentication/happens_lazily')

            assert self.client.config._auth_token is None
            assert self.client.config.auth_token is not None

    def test_authentication_can_reuse_an_auth_token(self):
        special_client = Client(None, None, Config.ENV_DEMO)
        special_client.config.auth_token = "deadbeefdeadbeefdeadbeefdeadbeef"

        with Betamax(special_client.config.session) as betamax:
            betamax.use_cassette('authentication/can_use_just_a_token')

            response = special_client.beneficiaries.find()
            assert response is not None

    def test_authentication_can_be_closed(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('authentication/can_be_closed')

            assert self.client.config.auth_token is not None
            assert self.client.close_session() is True
            assert self.client.config._auth_token is None

    def test_authentication_handles_session_timeout(self):
        # Set the token to an invalid one
        self.client.config.auth_token = 'deadbeefdeadbeefdeadbeefdeadbeef'

        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('authentication/handles_session_timeout', match_requests_on=['uri', 'method'])

            response = self.client.beneficiaries.find()

            assert response is not None
