import pytest
from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import Beneficiary
from currencycloud.http import Http


class TestAuthentication:
    def setup_method(self, method):
        login_id = 'rjnienaber@gmail.com'
        api_key = 'ef0fd50fca1fb14c1fab3a8436b9ecb65f02f129fd87eafa45ded8ae257528f0'
        environment = Config.ENV_DEMONSTRATION

        self.client = Client(login_id, api_key, environment)

    def test_authentication_happens_lazily(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('authentication/happens_lazily')

            assert self.client.config._auth_token is None
            assert self.client.config.auth_token is not None

    def test_authentication_can_reuse_an_auth_token(self):
        special_client = Client(None, None, Config.ENV_DEMONSTRATION)
        special_client.config.auth_token = self.client.config.auth_token

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
