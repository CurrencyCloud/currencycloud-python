import pytest
from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import *
from currencycloud.errors import NotFoundError, BadRequestError


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
            assert payment.currency == "GBP"

            TestPayments.paymentId = payment.id

    def test_payments_can_validate(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/validate')

            payment = self.client.payments.validate(currency="GBP",
                                                  beneficiary_id="a0bd2d78-3621-4c29-932f-a39d6b34d5e7",
                                                  amount="1000",
                                                  reason="Testing payments",
                                                  reference="Testing payments",
                                                  payment_type="regular")

            assert payment is not None
            assert isinstance(payment, PaymentValidation)

            assert payment.validation_result == "success"

    def test_payments_can_validate_and_create_with_sca(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/validate_and_create_with_sca')

            payment_validation_result = self.client.payments.validate(currency="GBP",
                                                  beneficiary_id="a0bd2d78-3621-4c29-932f-a39d6b34d5e7",
                                                  amount="1000",
                                                  reason="Testing SCA payments",
                                                  reference="Testing SCA payments",
                                                  payment_type="regular", 
                                                  sca_to_authenticated_user=True)
            assert payment_validation_result is not None
            assert isinstance(payment_validation_result, PaymentValidation)
            assert payment_validation_result.validation_result == "success"
            assert hasattr(payment_validation_result, 'response_headers')
            assert 'x-sca-id' in payment_validation_result.response_headers
            assert 'x-sca-type' in payment_validation_result.response_headers
            assert 'x-sca-required' in payment_validation_result.response_headers
            assert payment_validation_result.response_headers['x-sca-id'] == 'e99c5fb0-88b2-47b6-b9ea-77279fdb3fc2'
            assert payment_validation_result.response_headers['x-sca-required'] == 'true'
            assert payment_validation_result.response_headers['x-sca-type'] == 'SMS'

            payment = self.client.payments.create(currency="GBP",
                                                  beneficiary_id="a0bd2d78-3621-4c29-932f-a39d6b34d5e7",
                                                  amount="1000",
                                                  reason="Testing SCA payments",
                                                  reference="Testing SCA payments",
                                                  payment_type="regular",
                                                  sca_id=payment_validation_result.response_headers['x-sca-id'],
                                                  sca_token="123456")
            assert payment is not None
            assert isinstance(payment, Payment)
            assert payment.id is not None
            assert payment.currency == "GBP"
            TestPayments.paymentId = payment.id

    def test_payments_validate_raises_on_missing_details(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/validate_error')

            with pytest.raises(BadRequestError) as excinfo:
                payment = self.client.payments.validate(currency="GBP",
                                                      beneficiary_id="a0bd2d78-3621-4c29-932f-a39d6b34d5e7",
                                                      reason="Testing payments",
                                                      reference="Testing payments",
                                                      payment_type="regular")
                raise Exception('Should raise exception')

            assert True

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

            payment = self.client.payments.retrieve(TestPayments.paymentId, with_deleted=True)

            assert payment is not None
            assert isinstance(payment, Payment)

            assert payment.id == TestPayments.paymentId

    def test_payments_can_retrieve_submission_info_mt103(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/retrieve_submission_info_mt103')

            payment_id = "01d8c0bc-7f0c-4cdd-bc7e-ef81f68500fe"
            submission = self.client.payments.retrieve_submission_info(payment_id)

            assert submission is not None
            assert "status" in submission
            assert submission["status"] == "pending"
            assert "submission_ref" in submission
            assert submission["submission_ref"] == "MXGGYAGJULIIQKDV"
            assert "format" in submission
            assert submission["format"] == "MT103"
            assert "message" in submission

    def test_payments_can_retrieve_submission_info_pac008(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/retrieve_submission_info_pac008')

            payment_id = "bea7b94c-e4c8-4629-b01f-9e6630264356"
            submission = self.client.payments.retrieve_submission_info(payment_id)

            assert submission is not None
            assert "status" in submission
            assert submission["status"] == "pending"
            assert "submission_ref" in submission
            assert submission["submission_ref"] == "GFYQQJHFWIUTPHFN"
            assert "format" in submission
            assert submission["format"] == "PACS008"
            assert "message" in submission

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

    def test_payments_can_confirm(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/payments_confirmation')

            payment = self.client.payments.payment_confirmation('a739b199-8260-4ffa-a404-b4b58345332e')

            assert payment is not None
            assert payment.id is not None
            assert payment.payment_id == 'a739b199-8260-4ffa-a404-b4b58345332e'
            assert payment.account_id is not None

    def test_payments_can_authorise(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/authorise')
            beneficiary = self.client.beneficiaries.create(bank_account_holder_name="Test User",
                                                           bank_country="GB",
                                                           currency="GBP",
                                                           name="Test User",
                                                           account_number="12345678",
                                                           routing_code_type_1="sort_code",
                                                           routing_code_value_1="123456")
            payment = self.client.payments.create(currency="GBP",
                                                  beneficiary_id=beneficiary.id,
                                                  amount="1000",
                                                  reason="Testing payments",
                                                  reference="Testing payments",
                                                  payment_type="regular")
            self.client.config.login_id = 'development2@currencycloud.demo'
            self.client.config.api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
            self.client.config.reauthenticate()
            payment = self.client.payments.authorise(payment_ids=[TestPayments.paymentId])
            assert payment is not None
            self.client.config.login_id = 'development@currencycloud.demo'
            self.client.config.api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
            self.client.config.reauthenticate()

    def test_payments_delivery_date(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/delivery_date')

            payment = self.client.payments.payment_delivery_date(payment_date='2018-01-01', payment_type='regular', currency='EUR', bank_country='IT')

            assert payment is not None
            assert isinstance(payment, Payment)

    def test_quote_payment_fee(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/quote_payment_fee')

            quote_payment_fee = self.client.payments.quote_payment_fee(payment_currency='USD', payment_destination_country='US', payment_type='regular')

            assert quote_payment_fee is not None
            assert isinstance(quote_payment_fee, QuotePaymentFee)
            assert quote_payment_fee.account_id == "0534aaf2-2egg-0134-2f36-10b11cd33cfb"
            assert quote_payment_fee.fee_amount == "10.00"
            assert quote_payment_fee.fee_currency == "EUR"
            assert quote_payment_fee.payment_currency == "USD"
            assert quote_payment_fee.payment_destination_country == "US"
            assert quote_payment_fee.payment_type == "regular"
            assert quote_payment_fee.charge_type is None

    def test_payments_delivery_date_error_response(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/delivery_date_error')
            with pytest.raises(BadRequestError):
                self.client.payments.payment_delivery_date(payment_date='2020-08-02', payment_type='priority', currency='USD', bank_country='CA')

    def test_payments_delivery_date_error_response2(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/delivery_date_error2')
            with pytest.raises(BadRequestError):
                self.client.payments.payment_delivery_date(payment_date='2020-08-02', payment_type='priority', currency='USD', bank_country='abc')

    def test_tracking_info(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/tracking_info')

            tracking_info = self.client.payments.tracking_info("46ed4827-7b6f-4491-a06f-b548d5a7512d")

            assert tracking_info is not None
            assert isinstance(tracking_info, PaymentTrackingInfo)
            assert tracking_info.uetr == "46ed4827-7b6f-4491-a06f-b548d5a7512d"
            assert tracking_info.transaction_status["status"] == "processing"
            assert len(tracking_info.payment_events) == 7

    def test_can_retry_payment_notifications(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('payments/retry_payment_notifications')

            # Should fail on invalid notification_type
            with pytest.raises(BadRequestError) as excinfo:
                self.client.payments.retry_payment_notifications("46ed4827-7b6f-4491-a06f-b548d5a7512d", notification_type="payment_notification")
                raise Exception('Should raise exception')
            assert True

            resp = self.client.payments.retry_payment_notifications("46ed4827-7b6f-4491-a06f-b548d5a7512d",
                                                             notification_type="payment_released_notification")
            assert resp is not None

