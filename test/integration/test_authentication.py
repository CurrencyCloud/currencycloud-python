import pytest
from betamax import Betamax

import currencycloud
from currencycloud import config
from currencycloud.errors import *
from currencycloud.resources import Beneficiary

from currencycloud.response_handler import ResponseHandler


class TestAuthentication:
    session_token = None

    def setup_method(self, method):
        config.DEBUG = False

        currencycloud.reset_session()
        currencycloud.environment = currencycloud.ENV_DEMOSTRATION
        currencycloud.login_id = 'rjnienaber@gmail.com'
        currencycloud.api_key = 'ef0fd50fca1fb14c1fab3a8436b9ecb65f02f129fd87eafa45ded8ae257528f0'
        currencycloud.token = None

    def teardown(self):
        config.DEBUG = False

    def test_authentication_happens_lazily(self):
        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette('authentication/happens_lazily')

            TestAuthentication.session_token = currencycloud.session().token

            assert currencycloud.session() is not None
            assert currencycloud.session().token is not None
            assert currencycloud.session().token

    def test_authentication_can_use_just_a_token(self):
        currencycloud.login_id = None
        currencycloud.api_key = None
        currencycloud.token = TestAuthentication.session_token

        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette('authentication/can_use_just_a_token')

            response = Beneficiary.find()

            assert response is not None

    def test_authentication_can_be_closed(self):
        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette('authentication/can_be_closed')

            assert currencycloud.session() is not None
            assert currencycloud.close_session() is True

    def test_authentication_handles_session_timeout(self):
        currencycloud.token = '3907f05da86533710efc589d58f51f45'

        # WARNING!
        # we need to disable recording becouse this cassette
        # generates incompatible files among different Python versions!

        # session = currencycloud.session(authenticate=False)
        # with Betamax(session.requests_session) as betamax:
        #     betamax.use_cassette('authentication/handles_session_timeout', match_requests_on=['uri', 'method', 'headers'])

        response = Beneficiary.find()

        assert response is not None
