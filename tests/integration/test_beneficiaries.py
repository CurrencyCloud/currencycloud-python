import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *
from currencycloud.errors import BadRequestError


class TestBeneficiaries:
    def setup_method(self, method):
        login_id = 'api.test.user1@currencycloud.com'
        api_key = '0a14256abc393cdc238672b2d42d54f5581937f3ee23b76d5cfa842f63f8364d'
        environment = Config.ENV_DEMONSTRATION

        self.client = Client(login_id, api_key, environment)

    def test_beneficiaries_can_create(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('beneficiaries/create')

            beneficiary = self.client.beneficiaries.create(bank_account_holder_name="Test User",
                                                           bank_country="GB",
                                                           currency="GBP",
                                                           name="Test User",
                                                           account_number="12345678",
                                                           routing_code_type_1="sort_code",
                                                           routing_code_value_1="123456")

            assert beneficiary is not None
            assert isinstance(beneficiary, Beneficiary)

            assert beneficiary.id is not None
            assert beneficiary.bank_country == "GB"

    def test_beneficiaries_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('beneficiaries/find')

            beneficiaries = self.client.beneficiaries.find(account_number="12345678", per_page=1)

            assert beneficiaries
            assert len(beneficiaries) == 1

            beneficiary = beneficiaries[0]

            assert beneficiary is not None
            assert isinstance(beneficiary, Beneficiary)

            assert beneficiary.account_number == "12345678"

    def test_beneficiaries_can_retrieve(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('beneficiaries/retrieve')

            beneficiary = self.client.beneficiaries.retrieve("a0bd2d78-3621-4c29-932f-a39d6b34d5e7")

            assert beneficiary is not None
            assert isinstance(beneficiary, Beneficiary)

            assert beneficiary.id == "a0bd2d78-3621-4c29-932f-a39d6b34d5e7"

    def test_beneficiaries_can_update(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('beneficiaries/update')

            beneficiary = self.client.beneficiaries.retrieve("a0bd2d78-3621-4c29-932f-a39d6b34d5e7")
            assert beneficiary is not None

            beneficiary.account_number = "87654321"
            beneficiary.update()
            assert beneficiary.account_number == "87654321"

            beneficiary = self.client.beneficiaries.retrieve("a0bd2d78-3621-4c29-932f-a39d6b34d5e7")
            assert beneficiary is not None
            assert beneficiary.account_number == "87654321"


    def test_beneficiaries_can_validate(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('beneficiaries/validate')

            beneficiary = self.client.beneficiaries.validate(bank_country="GB",
                                                             currency="GBP",
                                                             beneficiary_country="GB",
                                                             account_number="12345678",
                                                             routing_code_type_1="sort_code",
                                                             routing_code_value_1="123456")

            assert beneficiary is not None
            assert isinstance(beneficiary, Beneficiary)

            assert beneficiary.bank_country == "GB"

    def test_beneficiaries_validate_raises_on_missing_details(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('beneficiaries/validate_error')


            with pytest.raises(BadRequestError) as excinfo:
                beneficiary = self.client.beneficiaries.validate(bank_country="GB",
                                                                 currency="GBP",
                                                                 beneficiary_country="GB")
                raise Exception('Should raise exception')

            assert True
