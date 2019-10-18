from betamax import Betamax

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

    def test_reference_can_retrieve_payment_purpose_codes(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('reference/can_retrieve_payment_purpose_codes')

            details = self.client.reference.payment_purpose_codes(currency='CNY')
            assert len(details) > 0

            purpose_code = details[0]
            assert isinstance(purpose_code, PaymentPurposeCode)

            assert purpose_code.currency == 'CNY'
            assert purpose_code.entity_type == 'company'
            assert purpose_code.purpose_code == 'current_account_payment'

    def test_reference_can_retrieve_bank_details(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('reference/can_retrieve_bank_details')

            details = self.client.reference.bank_details(identifier_type="iban", identifier_value="GB19TCCL00997901654515")

            assert isinstance(details, BankDetails)

            assert details.account_number == "GB19TCCL00997901654515"
            assert details.bank_address == "12 STEWARD STREET  THE STEWARD BUILDING FLOOR 0"
            assert details.bank_branch == ""
            assert details.bank_city == "LONDON"
            assert details.bank_country == "UNITED KINGDOM"
            assert details.bank_country_ISO == "GB"
            assert details.bank_name == "THE CURRENCY CLOUD LIMITED"
            assert details.bank_post_code == "E1 6FQ"
            assert details.bank_state == "LONDON"
            assert details.bic_swift == "TCCLGB22XXX"
            assert details.currency is None
            assert details.identifier_type == "iban"
            assert details.identifier_value == "GB19TCCL00997901654515"

    def test_reference_can_retrieve_payment_fee_rules(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('reference/can_retrieve_payment_fee_rules')

            payment_fee_rules1 = self.client.reference.payment_fee_rules()
            assert len(payment_fee_rules1) == 3

            fee_rule1_1 = payment_fee_rules1[0]
            assert isinstance(fee_rule1_1, PaymentFeeRule)
            assert fee_rule1_1.charge_type == "shared"
            assert fee_rule1_1.fee_amount == "2.00"
            assert fee_rule1_1.fee_currency == "AED"
            assert fee_rule1_1.payment_type == "priority"

            fee_rule1_2 = payment_fee_rules1[1]
            assert isinstance(fee_rule1_2, PaymentFeeRule)
            assert fee_rule1_2.charge_type == "shared"
            assert fee_rule1_2.fee_amount == "12.00"
            assert fee_rule1_2.fee_currency == "USD"
            assert fee_rule1_2.payment_type == "regular"

            fee_rule1_3 = payment_fee_rules1[2]
            assert isinstance(fee_rule1_3, PaymentFeeRule)
            assert fee_rule1_3.charge_type == "ours"
            assert fee_rule1_3.fee_amount == "5.25"
            assert fee_rule1_3.fee_currency == "GBP"
            assert fee_rule1_3.payment_type == "priority"

            payment_fee_rules2 = self.client.reference.payment_fee_rules(payment_type='regular')
            assert len(payment_fee_rules2) == 1

            fee_rule2_1 = payment_fee_rules2[0]
            assert isinstance(fee_rule2_1, PaymentFeeRule)
            assert fee_rule2_1.charge_type == "shared"
            assert fee_rule2_1.fee_amount == "12.00"
            assert fee_rule2_1.fee_currency == "USD"
            assert fee_rule2_1.payment_type == "regular"

            payment_fee_rules3 = self.client.reference.payment_fee_rules(charge_type='ours')
            assert len(payment_fee_rules3) == 1

            fee_rule3_1 = payment_fee_rules3[0]
            assert isinstance(fee_rule3_1, PaymentFeeRule)
            assert fee_rule3_1.charge_type == "ours"
            assert fee_rule3_1.fee_amount == "5.25"
            assert fee_rule3_1.fee_currency == "GBP"
            assert fee_rule3_1.payment_type == "priority"

