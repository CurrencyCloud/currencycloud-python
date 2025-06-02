from betamax import Betamax

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
            assert iban.iban_code == "GB33BUKB20201555555555"
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
