import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re
import sys

import currencycloud
from currencycloud.errors import *
from currencycloud.resources import *


def is_string(s):
    if sys.version_info[0] < 3:
        return isinstance(s, basestring)
    else:
        return isinstance(s, str)


class TestActions:
    beneficiary_id = None
    beneficiary_first_id = None
    beneficiary_params = {
        'beneficiary_entity_type': 'individual',
        'beneficiary_first_name': 'Dr.',
        'beneficiary_last_name': 'Who',
        'beneficiary_address': ['Address 42'],
        'beneficiary_city': 'The Citadel',
        'beneficiary_postcode': '42424',
        'beneficiary_country': 'GB',
        'bank_account_holder_name': 'Test User',
        'bank_country': 'GB',
        'currency': 'GBP',
        'name': 'Test User Nick',
        'account_number': '4185 4372',
        'routing_code_type_1': 'aba',
        'routing_code_value_1': '123456780',
        'routing_code_type_2': 'sort_code',
        'routing_code_value_2': '400730',
        'payment_types': ['priority', 'regular']
    }

    def setup_method(self, method):
        currencycloud.reset_session()
        currencycloud.environment = currencycloud.ENV_DEMOSTRATION
        currencycloud.login_id = 'rjnienaber@gmail.com'
        currencycloud.api_key = 'ef0fd50fca1fb14c1fab3a8436b9ecb65f02f129fd87eafa45ded8ae257528f0'  # noqa
        currencycloud.token = None

    def test_actions_can_create(self):
        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette('actions/can_create')

            beneficiary = Beneficiary.create(**TestActions.beneficiary_params)

            TestActions.beneficiary_id = beneficiary.id

            assert isinstance(beneficiary, Beneficiary)
            assert beneficiary.id
            assert beneficiary.created_at
            assert beneficiary.updated_at
            assert beneficiary.created_at == beneficiary.updated_at

            for k, v in TestActions.beneficiary_params.items():
                if k in ('routing_code_type_1', 'routing_code_value_1'):
                    # skip fields with wrong values that are cleaned up by the
                    # API
                    continue
                b = beneficiary[k]
                if is_string(v):
                    b = str(b)
                    v = str(v)
                assert b == v

    def test_actions_can_retrieve(self):
        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette('actions/can_retrieve')

            beneficiary = Beneficiary.retrieve(TestActions.beneficiary_id)

            assert isinstance(beneficiary, Beneficiary)
            assert beneficiary.id == TestActions.beneficiary_id

    def test_actions_can_find(self):
        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette('actions/can_find')

            beneficiaries = Beneficiary.find(
                bank_account_holder_name=TestActions.beneficiary_params['bank_account_holder_name'])  # noqa

            assert beneficiaries
            assert len(beneficiaries) >= 1

            TestActions.beneficiary_first_id = beneficiaries[0].id

            for beneficiary in beneficiaries:
                assert isinstance(beneficiary, Beneficiary)

            pagination = beneficiaries.pagination

            assert pagination.total_entries > 0
            assert pagination.current_page == 1
            assert pagination.per_page == 25
            assert pagination.previous_page == -1
            assert pagination.order == 'created_at'
            assert pagination.order_asc_desc == 'asc'

    def test_actions_can_first(self):
        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette('actions/can_first')

            beneficiary = Beneficiary.first(
                bank_account_holder_name=TestActions.beneficiary_params['bank_account_holder_name'])  # noqa

            assert isinstance(beneficiary, Beneficiary)
            assert beneficiary.id == TestActions.beneficiary_first_id
            assert beneficiary.bank_account_holder_name == TestActions.beneficiary_params[  # noqa
                'bank_account_holder_name']

    def test_actions_can_update(self):
        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette('actions/can_update')

            beneficiary = Beneficiary.update_id(
                TestActions.beneficiary_id,
                bank_account_holder_name="Test Name 2"
            )

            assert isinstance(beneficiary, Beneficiary)
            assert beneficiary.id == TestActions.beneficiary_id
            assert beneficiary.bank_account_holder_name == "Test Name 2"
            assert beneficiary.changed is False

    def test_actions_can_delete(self):
        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette('actions/can_delete')

            beneficiary = Beneficiary.delete_id(TestActions.beneficiary_id)

            assert isinstance(beneficiary, Beneficiary)
            assert beneficiary.id == TestActions.beneficiary_id
            assert beneficiary.bank_account_holder_name == "Test Name 2"

    def test_actions_can_current(self):
        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette('actions/can_current')

            account = Account.current()

            assert isinstance(account, Account)
            assert account.id == '8ec3a69b-02d1-4f09-9a6b-6bd54a61b3a8'
            assert account.created_at == '2015-04-24T15:57:55+00:00'

    def test_actions_can_validate_beneficiaries(self):
        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette('actions/can_validate_beneficiaries')

            params = {
                'bank_country': 'GB',
                'currency': 'GBP',
                'account_number': TestActions.beneficiary_params['account_number'],  # noqa
                'routing_code_type_1': TestActions.beneficiary_params['routing_code_type_2'],  # noqa
                'routing_code_value_1': TestActions.beneficiary_params['routing_code_value_2'],  # noqa
                'payment_types': ['regular']}

            beneficiary = Beneficiary.validate(**params)

            assert isinstance(beneficiary, Beneficiary)
            assert beneficiary.account_number == TestActions.beneficiary_params[  # noqa
                'account_number']
            assert 'regular' in beneficiary.payment_types

    def test_actions_can_use_currency_to_retrieve_balance(self):
        session = currencycloud.session(authenticate=False)
        with Betamax(session.requests_session) as betamax:
            betamax.use_cassette(
                'actions/can_use_currency_to_retrieve_balance')

            balance = Balance.currency_with_code('GBP')

            assert isinstance(balance, Balance)
            assert balance.id
