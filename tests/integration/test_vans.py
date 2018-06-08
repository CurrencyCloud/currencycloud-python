import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *


class TestVans:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_vans_can_get_for_sub_account(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('vans/can_get_for_sub_account')

            vans = self.client.vans.retrieve_subaccounts("00d272ee-fae5-4f97-b425-993a2d6e3a46")
            assert vans
            assert len(vans) == 1

            van = vans[0]

            assert van is not None
            assert isinstance(van, Van)

            assert van.id == "00d272ee-fae5-4f97-b425-993a2d6e3a46"
            assert van.account_id == "2090939e-b2f7-3f2b-1363-4d235b3f58af"
            assert van.virtual_account_number == "8303723297"
            assert van.account_holder_name == "Account-ZXOANNAMKPRQ"
            assert van.bank_institution_name == "Community Federal Savings Bank"
            assert van.bank_institution_address == "Seventh Avenue, New York, NY 10019, US"
            assert van.bank_institution_country == "United States"
            assert van.routing_code == "026073150"

            pagination = vans.pagination

            assert pagination.total_entries == 1
            assert pagination.total_pages == 1
            assert pagination.current_page == 1
            assert pagination.per_page == 25
            assert pagination.previous_page == -1
            assert pagination.next_page == 2
            assert pagination.order == 'created_at'
            assert pagination.order_asc_desc == 'asc'

    def test_vans_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('vans/can_find')

            vans = self.client.vans.find(per_page=1)
            assert vans
            assert len(vans) == 1

            van = vans[0]

            assert van is not None
            assert isinstance(van, Van)

            assert van.id == "00d272ee-fae5-4f97-b425-993a2d6e3a46"
            assert van.account_id == "2090939e-b2f7-3f2b-1363-4d235b3f58af"
            assert van.virtual_account_number == "8303723297"
            assert van.account_holder_name == "Account-ZXOANNAMKPRQ"
            assert van.bank_institution_name == "Community Federal Savings Bank"
            assert van.bank_institution_address == "Seventh Avenue, New York, NY 10019, US"
            assert van.bank_institution_country == "United States"
            assert van.routing_code == "026073150"

            pagination = vans.pagination

            assert pagination.total_entries == 1
            assert pagination.total_pages == 1
            assert pagination.current_page == 1
            assert pagination.per_page == 25
            assert pagination.previous_page == -1
            assert pagination.next_page == 2
            assert pagination.order == 'created_at'
            assert pagination.order_asc_desc == 'asc'

    def test_vans_can_find_for_sub_account(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('vans/can_find_for_sub_account')

            vans = self.client.vans.find_subaccounts(per_page=1)
            assert vans
            assert len(vans) == 1

            van = vans[0]

            assert van is not None
            assert isinstance(van, Van)

            assert van.id == "00d272ee-fae5-4f97-b425-993a2d6e3a46"
            assert van.account_id == "2090939e-b2f7-3f2b-1363-4d235b3f58af"
            assert van.virtual_account_number == "8303723297"
            assert van.account_holder_name == "Account-ZXOANNAMKPRQ"
            assert van.bank_institution_name == "Community Federal Savings Bank"
            assert van.bank_institution_address == "Seventh Avenue, New York, NY 10019, US"
            assert van.bank_institution_country == "United States"
            assert van.routing_code == "026073150"

            pagination = vans.pagination

            assert pagination.total_entries == 1
            assert pagination.total_pages == 1
            assert pagination.current_page == 1
            assert pagination.per_page == 25
            assert pagination.previous_page == -1
            assert pagination.next_page == 2
            assert pagination.order == 'created_at'
            assert pagination.order_asc_desc == 'asc'

