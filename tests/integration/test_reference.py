import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *


class TestReference:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_reference_can_retrieve_beneficiary_required_details(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('reference/can_retrieve_beneficiary_required_details')

            details = self.client.reference.beneficiary_required_details(
                currency='GBP',
                bank_account_country='GB',
                beneficiary_country='GB'
            )

            assert len(details) > 0

            details = details[0]

            assert isinstance(details, BeneficiaryRequiredDetails)
            assert details.beneficiary_entity_type == 'individual'
            assert details.payment_type == 'priority'
            assert details.beneficiary_address == "^.{1,255}"
            assert details.beneficiary_city == "^.{1,255}"
            assert details.beneficiary_country == "^[A-z]{2}$"
            assert details.beneficiary_first_name == "^.{1,255}"
            assert details.beneficiary_last_name == "^.{1,255}"
            assert details.acct_number == "^[0-9A-Z]{1,50}$"
            assert details.sort_code == "^\\d{6}$"

    def test_reference_can_retrieve_conversion_dates(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('reference/can_retrieve_conversion_dates')

            dates = self.client.reference.conversion_dates(conversion_pair='GBPUSD')

            assert isinstance(dates, ConversionDates)
            assert dates.first_conversion_date
            assert dates.default_conversion_date
            assert 'No trading on Saturday' in dates.invalid_conversion_dates.values()  # noqa

    def test_reference_can_retrieve_currencies(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('reference/can_retrieve_currencies')

            currencies = self.client.reference.currencies()

            assert len(currencies) > 0

            currency = currencies[0]

            assert isinstance(currency, Currency)
            assert currency.code == 'AED'
            assert currency.name == 'United Arab Emirates Dirham'
            assert currency.decimal_places == 2

    def test_reference_can_retrieve_settlement_accounts(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('reference/can_retrieve_settlement_accounts')

            settlement_accounts = self.client.reference.settlement_accounts(currency='GBP')

            assert len(settlement_accounts) > 0

            settlement_account = settlement_accounts[0]

            assert isinstance(settlement_account, SettlementAccount)
            assert settlement_account.bank_name
            assert 'The Currency Cloud GBP' in settlement_account.bank_account_holder_name  # noqa

    def test_reference_can_retrieve_payer_required_details(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('reference/can_retrieve_payer_required_details')

            details = self.client.reference.payer_required_details(payer_country='GB')

            assert len(details) > 0

            details = details[0]

            assert isinstance(details, PayerRequiredDetails)
            assert details.payer_entity_type == 'company'
            assert details.payment_type == 'priority'
            assert details.payer_identification_type == 'incorporation_number'
            assert details.required_fields[0]["name"] == 'payer_country'
            assert details.required_fields[0]["validation_rule"] == '^[A-z]{2}$'
            assert details.required_fields[1]["name"] == 'payer_city'
            assert details.required_fields[1]["validation_rule"] == '^.{1,255}'
            assert details.required_fields[2]["name"] == 'payer_address'
            assert details.required_fields[2]["validation_rule"] == '^.{1,255}'
            assert details.required_fields[3]["name"] == 'payer_company_name'
            assert details.required_fields[3]["validation_rule"] == '^.{1,255}'
            assert details.required_fields[4]["name"] == 'payer_identification_value'
            assert details.required_fields[4]["validation_rule"] == '^.{1,255}'
