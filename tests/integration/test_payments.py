import pytest
from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.errors import NotFoundError
from currencycloud.resources import *


class TestPayments:
    paymentId = None

    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

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
            assert payment.amount == '1000.00'
            assert payment.beneficiary_id == 'a0bd2d78-3621-4c29-932f-a39d6b34d5e7'
            assert payment.currency == "GBP"
            assert payment.reference == 'Testing payments'
            assert payment.reason == 'Testing payments'
            assert payment.status is not None
            assert payment.creator_contact_id is not None
            assert payment.payment_type == 'regular'
            assert payment.payment_date is not None
            assert payment.transferred_at is not None
            assert payment.authorisation_steps_required is not None
            assert payment.last_updater_contact_id is not None
            assert payment.short_reference is not None
            assert payment.conversion_id is None
            assert payment.failure_reason is not None
            assert payment.payer_id is not None
            assert payment.payer_details_source is not None
            assert payment.created_at is not None
            assert payment.updated_at is not None
            assert payment.payment_group_id is None
            assert payment.unique_request_id is None

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

            assert payment.id is not None
            assert payment.amount == '1000.00'
            assert payment.beneficiary_id == 'a0bd2d78-3621-4c29-932f-a39d6b34d5e7'
            assert payment.currency == "GBP"
            assert payment.reference == 'Testing payments'
            assert payment.reason == 'Testing payments'
            assert payment.status is not None
            assert payment.creator_contact_id is not None
            assert payment.payment_type == 'regular'
            assert payment.payment_date is not None
            assert payment.transferred_at is not None
            assert payment.authorisation_steps_required is not None
            assert payment.last_updater_contact_id is not None
            assert payment.short_reference is not None
            assert payment.conversion_id is None
            assert payment.failure_reason is not None
            assert payment.payer_id is not None
            assert payment.payer_details_source is not None
            assert payment.created_at is not None
            assert payment.updated_at is not None
            assert payment.payment_group_id is None
            assert payment.unique_request_id is None

    def test_payments_can_retrieve(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/retrieve')

            payment = self.client.payments.retrieve(TestPayments.paymentId)

            assert payment is not None
            assert isinstance(payment, Payment)

            assert payment.id == TestPayments.paymentId
            assert payment.amount == '1000.00'
            assert payment.beneficiary_id == 'a0bd2d78-3621-4c29-932f-a39d6b34d5e7'
            assert payment.currency == "GBP"
            assert payment.reference == 'Testing payments'
            assert payment.reason == 'Testing payments'
            assert payment.status is not None
            assert payment.creator_contact_id is not None
            assert payment.payment_type == 'regular'
            assert payment.payment_date is not None
            assert payment.transferred_at is not None
            assert payment.authorisation_steps_required is not None
            assert payment.last_updater_contact_id is not None
            assert payment.short_reference is not None
            assert payment.conversion_id is None
            assert payment.failure_reason is not None
            assert payment.payer_id is not None
            assert payment.payer_details_source is not None
            assert payment.created_at is not None
            assert payment.updated_at is not None
            assert payment.payment_group_id is None
            assert payment.unique_request_id is None

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
            assert payment.id is not None
            assert payment.amount == "1200.00"
            assert payment.beneficiary_id == 'a0bd2d78-3621-4c29-932f-a39d6b34d5e7'
            assert payment.currency == "GBP"
            assert payment.reference == 'Testing payments'
            assert payment.reason == 'Testing payments'
            assert payment.status is not None
            assert payment.creator_contact_id is not None
            assert payment.payment_type == 'regular'
            assert payment.payment_date is not None
            assert payment.transferred_at is not None
            assert payment.authorisation_steps_required is not None
            assert payment.last_updater_contact_id is not None
            assert payment.short_reference is not None
            assert payment.conversion_id is None
            assert payment.failure_reason is not None
            assert payment.payer_id is not None
            assert payment.payer_details_source is not None
            assert payment.created_at is not None
            assert payment.updated_at is not None
            assert payment.payment_group_id is None
            assert payment.unique_request_id is None

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

    def test_payments_can_confirm(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/payments_confirmation')

            payment = self.client.payments.payment_confirmation('a739b199-8260-4ffa-a404-b4b58345332e')

            assert payment is not None
            assert payment.id is not None
            assert payment.payment_id == 'a739b199-8260-4ffa-a404-b4b58345332e'
            assert payment.account_id is not None

