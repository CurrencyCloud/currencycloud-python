import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *
from currencycloud.errors import NotFoundError


class TestPayments:
    paymentId = None

    def setup_method(self, method):
        login_id = 'api.test.user1@currencycloud.com'
        api_key = '0a14256abc393cdc238672b2d42d54f5581937f3ee23b76d5cfa842f63f8364d'
        environment = Config.ENV_DEMONSTRATION

        self.client = Client(login_id, api_key, environment)

    def test_payments_can_create(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/create')

            payment = self.client.payments.create(currency="GBP",
                                                  beneficiary_id="a0bd2d78-3621-4c29-932f-a39d6b34d5e7",
                                                  amount="1000",
                                                  reason="Testing payments",
                                                  reference="Testing payments",
                                                  payment_type="regular")

            assert payment is not None
            assert isinstance(payment, Payment)

            assert payment.id is not None
            assert payment.currency == "GBP"

            TestPayments.paymentId = payment.id

    def test_payments_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/find')

            payments = self.client.payments.find(currency="GBP", per_page=1)

            assert payments
            assert len(payments) == 1

            payment = payments[0]

            assert payment is not None
            assert isinstance(payment, Payment)

            assert payment.currency == "GBP"

    def test_payments_can_retrieve(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/retrieve')

            payment = self.client.payments.retrieve(TestPayments.paymentId)

            assert payment is not None
            assert isinstance(payment, Payment)

            assert payment.id == TestPayments.paymentId

    def test_payments_can_update(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/update')

            payment = self.client.payments.retrieve(TestPayments.paymentId)
            assert payment is not None

            payment.amount = "1200"
            payment.update()
            assert payment.amount == "1200"

            payment = self.client.payments.retrieve(TestPayments.paymentId)
            assert payment is not None
            assert payment.amount == "1200.00"

    def test_payments_can_delete(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/delete')

            payment = self.client.payments.retrieve(TestPayments.paymentId)
            assert payment is not None

            payment.delete()

            with pytest.raises(NotFoundError) as excinfo:
                payment = self.client.payments.retrieve(TestPayments.paymentId)
                raise Exception('Should raise exception')

            assert True
