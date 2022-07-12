import requests_mock

import currencycloud


class TestHttp:
    def setup_method(self):
        self.client = currencycloud.Client(None, None, currencycloud.Config.ENV_DEMO)
        self.client.config.auth_token = 'deadbeef'

    def test_http_on_behalf_of_in_get_request(self):
        with requests_mock.Mocker() as mock:
            def request_tester(request, context):
                assert 'on_behalf_of=d1f7f5c2-4187-41da-88fc-b3ae40fa958f' in request.url
                return {}

            self.client.config.on_behalf_of = 'd1f7f5c2-4187-41da-88fc-b3ae40fa958f'

            mock.get(
                requests_mock.ANY,
                status_code=200,
                json=request_tester)

            self.client.get('accounts/current')

    def test_http_on_behalf_of_in_post_request(self):
        with requests_mock.Mocker() as mock:
            def request_tester(request, context):
                assert 'on_behalf_of=d1f7f5c2-4187-41da-88fc-b3ae40fa958f' in request.body
                return {}

            self.client.config.on_behalf_of = 'd1f7f5c2-4187-41da-88fc-b3ae40fa958f'

            mock.post(
                requests_mock.ANY,
                status_code=201,
                json=request_tester)

            self.client.post('accounts/create', {'account_name': 'Test Account'})

    def test_http_on_behalf_of_ignored_if_none(self):
        with requests_mock.Mocker() as mock:
            def request_tester(request, context):
                assert 'on_behalf_of' not in request.body
                assert 'account_name=Test' in request.body
                return {}

            self.client.config.on_behalf_of = None

            mock.post(
                requests_mock.ANY,
                status_code=201,
                json=request_tester)

            self.client.post('accounts/create', {'account_name': 'Test Account'})

    def test_user_agent_in_header_of_in_post_request_unauthenticated(self):
        with requests_mock.Mocker() as mock:
            def request_tester(request, context):
                assert "User-Agent" in request.headers
                assert request.headers["User-Agent"] == currencycloud.Http.USER_AGENT
                assert "X-Auth-Token" not in request.headers
                return {"auth_token": "abc"}

            self.client.config.auth_token = None
            self.client.config.login_id = "Test"
            self.client.config.api_key = "Test"
            mock.post(
                requests_mock.ANY,
                status_code=200,
                json=request_tester)

            self.client.authenticate()

    def test_user_agent_in_header_of_in_get_request(self):
        with requests_mock.Mocker() as mock:
            def request_tester(request, context):
                assert "User-Agent" in request.headers
                assert request.headers["User-Agent"] == currencycloud.Http.USER_AGENT
                assert "X-Auth-Token" in request.headers
                return {}

            mock.get(
                requests_mock.ANY,
                status_code=200,
                json=request_tester)

            self.client.get('accounts/current')

    def test_user_agent_in_header_of_in_post_request(self):
        with requests_mock.Mocker() as mock:
            def request_tester(request, context):
                assert "User-Agent" in request.headers
                assert request.headers["User-Agent"] == currencycloud.Http.USER_AGENT
                assert "X-Auth-Token" in request.headers
                return {}

            mock.post(
                requests_mock.ANY,
                status_code=200,
                json=request_tester)

            self.client.post('accounts/create', {'account_name': 'Test Account'})

