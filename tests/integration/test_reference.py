import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *


class TestReference:
    def setup_method(self, method):
        login_id = 'rjnienaber@gmail.com'
        api_key = 'ef0fd50fca1fb14c1fab3a8436b9ecb65f02f129fd87eafa45ded8ae257528f0'
        environment = Config.ENV_DEMONSTRATION

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
