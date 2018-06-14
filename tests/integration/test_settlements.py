from betamax import Betamax

from currencycloud import Client, Config


class TestSettlements:
    settlement_id = None
    conversion_id = None

    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

        self.params = {
            'buy_currency': 'GBP',
            'sell_currency': 'USD',
            'fixed_side': 'buy',
            'amount': 1000,
            'reason': 'mortgage payment',
            'term_agreement': 'true'
        }

    def test_settlement_can_add_conversion(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('settlements/can_add_conversion')

            conversion = self.client.conversions.create(**self.params)
            settlement = self.client.settlements.create()
            updated_settlement = settlement.add_conversion(conversion.id)

            assert settlement is updated_settlement
            assert conversion.id in settlement.conversion_ids
            assert len(settlement.entries) > 0

            gbp_currency = settlement.entries[0]
            assert "GBP" in gbp_currency
            assert gbp_currency["GBP"] == {
                "receive_amount": "1000.00",
                "send_amount": "0.00"}

            usd_currency = settlement.entries[1]
            assert "USD" in usd_currency
            assert usd_currency['USD']['receive_amount'] == "0.00"
            assert usd_currency['USD']['send_amount']

            TestSettlements.settlement_id = settlement.id
            TestSettlements.conversion_id = conversion.id

    def test_settlement_can_release(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('settlements/can_release')

            settlement = self.client.settlements.retrieve(TestSettlements.settlement_id)
            released_settlement = settlement.release()

            assert released_settlement is settlement
            assert released_settlement.status == 'released'

    def test_settlement_can_unrelease(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('settlements/can_unrelease')

            settlement = self.client.settlements.retrieve(TestSettlements.settlement_id)
            unreleased_settlement = settlement.unrelease()

            assert unreleased_settlement is settlement
            assert not unreleased_settlement.released_at
            assert unreleased_settlement.status == 'open'

    def test_settlement_can_remove_conversion(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('settlements/can_remove_conversion')

            settlement = self.client.settlements.retrieve(TestSettlements.settlement_id)
            deleted_settlement = settlement.remove_conversion(TestSettlements.conversion_id)

            assert deleted_settlement is not None
            assert deleted_settlement.type == 'bulk'
            assert deleted_settlement.status == 'open'
            assert TestSettlements.conversion_id not in deleted_settlement.conversion_ids  # noqa
