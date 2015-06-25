import pytest
from mock import patch
import requests_mock

import currencycloud
from currencycloud.request_handler import RequestHandler
from currencycloud.session import Session

class TestRequestHandler:
    def setup(self):
        self.session = Session(currencycloud.ENV_DEMOSTRATION, None, None, '4df5b3e5882a412f148dcd08fa4e5b73')

    def test_request_handler_on_behalf_of_in_request(self):
       with requests_mock.Mocker() as mock:
            def request_tester(request, context):
                assert 'on_behalf_of=d1f7f5c2-4187-41da-88fc-b3ae40fa958f' in request.body

                return {}

            self.session.on_behalf_of = "d1f7f5c2-4187-41da-88fc-b3ae40fa958f"

            requestHandler = RequestHandler(self.session)
            mock.post(requestHandler.build_url('accounts/create'), status_code=200, json=request_tester)

            response = requestHandler.post('accounts/create', {'account_name': "Test Account"})

    def test_request_handler_on_behalf_of_ignored_invalid(self):
       with requests_mock.Mocker() as mock:
            def request_tester(request, context):
                assert 'on_behalf_of' not in request.body
                assert 'account_name=Test' in request.body

                return {}

            self.session.on_behalf_of = "nonsense variable"

            requestHandler = RequestHandler(self.session)
            mock.post(requestHandler.build_url('accounts/create'), status_code=200, json=request_tester)

            response = requestHandler.post('accounts/create', {'account_name': "Test Account"})
