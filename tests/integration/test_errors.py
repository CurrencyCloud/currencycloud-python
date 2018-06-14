from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.errors import AuthenticationError, BadRequestError, ForbiddenError, NotFoundError, TooManyRequestsError


class TestError:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_error_contains_full_details_for_api_error(self):
        login_id = 'non-existent-login-id'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeef'
        tmp_client = Client(login_id, api_key, Config.ENV_DEMO)

        with Betamax(tmp_client.config.session) as betamax:
            betamax.use_cassette('errors/contains_full_details_for_api_error')

            error = None
            try:
                tmp_client.auth.authenticate()
                raise Exception("Should have failed")
            except BadRequestError as e:
                error = e

        assert error is not None

        expected_error_fields = [
            "login_id: non-existent-login-id",
            "api_key: " + api_key,
            "verb: post",
            "url: https://devapi.currencycloud.com/v2/authenticate/api",
            "status_code: 400",
            "date:",
            "request_id:",
            "field: api_key",
            "code: api_key_length_is_invalid",
            "message: api_key should be 64 character(s) long",
            "length: 64"
        ]

        error_str = str(error)
        missing = False
        for f in expected_error_fields:
            if f not in error_str:
                missing = True
                break

        assert missing is False

    def test_error_is_raised_on_incorrect_authentication_details(self):
        login_id = 'non-existent-login-id'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        tmp_client = Client(login_id, api_key, Config.ENV_DEMO)

        with Betamax(tmp_client.config.session) as betamax:
            betamax.use_cassette('errors/is_raised_on_incorrect_authentication_details')

            error = None
            try:
                tmp_client.auth.authenticate()
                raise Exception("Should have failed")
            except AuthenticationError as e:
                error = e

            assert error.code == 'auth_failed'
            assert error.raw_response is not None
            assert error.status_code == 401
            assert len(error.messages) == 1

            error_message = error.messages[0]
            assert error_message.field == 'username'
            assert error_message.code == 'invalid_supplied_credentials'
            assert error_message.message == 'Authentication failed with the supplied credentials'  # noqa
            assert not error_message.params

    def test_error_is_raised_when_a_resource_is_not_found(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('errors/is_raised_when_a_resource_is_not_found')

            error = None
            try:
                self.client.beneficiaries.retrieve('081596c9-02de-483e-9f2a-4cf55dcdf98c')
                raise Exception("Should have failed")
            except NotFoundError as e:
                error = e

            assert error.code == 'beneficiary_not_found'
            assert error.raw_response is not None
            assert error.status_code == 404
            assert len(error.messages) == 1

            error_message = error.messages[0]
            assert error_message.field == 'id'
            assert error_message.code == 'beneficiary_not_found'
            assert error_message.message == 'Beneficiary was not found for this id'  # noqa
            assert not error_message.params

    def test_error_is_raised_when_too_many_requests_have_been_issued(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('errors/is_raised_when_too_many_requests_have_been_issued')

            error = None
            try:
                self.client.auth.authenticate()
                raise Exception("Should have failed")
            except TooManyRequestsError as e:
                error = e

            assert error.code == 'too_many_requests'
            assert error.raw_response is not None
            assert error.status_code == 429
            assert len(error.messages) == 1

            error_message = error.messages[0]
            assert error_message.field == 'base'
            assert error_message.code == 'too_many_requests'
            assert error_message.message == 'Too many requests have been made to the api. Please refer to the Developer Center for more information'  # noqa
            assert not error_message.params

    def test_error_is_raised_on_forbidden_request(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('errors/is_raised_on_forbidden_request')

            error = None
            try:
                self.client.transfers.find()
                raise Exception("Should have failed")
            except ForbiddenError as e:
                error = e

            assert error.code == 'permission_denied'
            assert error.raw_response is not None
            assert error.status_code == 403
            assert len(error.messages) == 1

            error_message = error.messages[0]
            assert error_message.code == 'permission_denied'
            assert error_message.message == "You do not have permission 'transfer_read' to perform this operation"
            assert not error_message.params
