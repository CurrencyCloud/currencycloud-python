import pytest
from mock import patch
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
