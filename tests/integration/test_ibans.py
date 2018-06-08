import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *


class TestIbans:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_ibans_can_get_for_sub_account(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('ibans/can_get_for_sub_account')

            ibans = self.client.ibans.retrieve_subaccounts("bd885485-bd74-414f-9add-ebadcd49f094")
            assert ibans
            assert len(ibans) == 1

            iban = ibans[0]

            assert iban is not None
            assert isinstance(iban, Iban)

            assert iban.id == "7f3bd9d2-e63b-4698-b74d-7e3aa209c788"
            assert iban.account_id == "bd885485-bd74-414f-9add-ebadcd49f094"
            assert iban.iban_code == "GB12TCCL00997921590081"
            assert iban.currency == "EUR"
            assert iban.account_holder_name == "Development"
            assert iban.bank_institution_name == "The Currency Cloud"
            assert iban.bank_institution_address == "12 Steward Street, The Steward Building, London, E1 6FQ, GB"
            assert iban.bank_institution_country == "United Kingdom"
            assert iban.bic_swift == "TCCLGB31"

            pagination = ibans.pagination

            assert pagination.total_entries == 1
            assert pagination.total_pages == 1
            assert pagination.current_page == 1
            assert pagination.per_page == 25
            assert pagination.previous_page == -1
            assert pagination.next_page == -1
            assert pagination.order == 'created_at'
            assert pagination.order_asc_desc == 'asc'

    def test_ibans_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('ibans/can_find')

            ibans = self.client.ibans.find(per_page=1)
            assert ibans
            assert len(ibans) == 1

            iban = ibans[0]

            assert iban is not None
            assert isinstance(iban, Iban)

            assert iban.id == "8242d1f4-4555-4155-a9bf-30feee785121"
            assert iban.account_id == "e277c9f9-679f-454f-8367-274b3ff977ff"
            assert iban.iban_code == "GB51TCCL00997961584807"
            assert iban.currency == "EUR"
            assert iban.account_holder_name == "Development CM"
            assert iban.bank_institution_name == "The Currency Cloud"
            assert iban.bank_institution_address == "12 Steward Street, The Steward Building, London, E1 6FQ, GB"
            assert iban.bank_institution_country == "United Kingdom"
            assert iban.bic_swift == "TCCLGB31"

            pagination = ibans.pagination

            assert pagination.total_entries == 1
            assert pagination.total_pages == 1
            assert pagination.current_page == 1
            assert pagination.per_page == 1
            assert pagination.previous_page == -1
            assert pagination.next_page == -1
            assert pagination.order == 'created_at'
            assert pagination.order_asc_desc == 'asc'

    def test_ibans_can_find_for_sub_account(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('ibans/can_find_for_sub_account')

            ibans = self.client.ibans.find_subaccounts(currency="EUR", per_page=1)
            assert ibans
            assert len(ibans) == 1

            iban = ibans[0]

            assert iban is not None
            assert isinstance(iban, Iban)

            assert iban.id == "7f3bd9d2-e63b-4698-b74d-7e3aa209c788"
            assert iban.account_id == "bd885485-bd74-414f-9add-ebadcd49f094"
            assert iban.iban_code == "GB12TCCL00997921590081"
            assert iban.currency == "EUR"
            assert iban.account_holder_name == "Development"
            assert iban.bank_institution_name == "The Currency Cloud"
            assert iban.bank_institution_address == "12 Steward Street, The Steward Building, London, E1 6FQ, GB"
            assert iban.bank_institution_country == "United Kingdom"
            assert iban.bic_swift == "TCCLGB31"

            pagination = ibans.pagination

            assert pagination.total_entries == 19
            assert pagination.total_pages == 19
            assert pagination.current_page == 1
            assert pagination.per_page == 1
            assert pagination.previous_page == -1
            assert pagination.next_page == 2
            assert pagination.order == 'created_at'
            assert pagination.order_asc_desc == 'asc'

