from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import *


class TestCollectionsScreening:
    def setup_method(self, method):
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_collections_screening_can_complete_accept(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('collections_screening/can_complete_accept')

            result = self.client.collections_screening.complete(
                "bdcca5e6-32fe-45f6-9476-6f8f518e6270",
                accepted=True,
                reason="accepted"
            )

            assert result is not None
            assert isinstance(result, CollectionsScreening)
            assert result.transaction_id == "bdcca5e6-32fe-45f6-9476-6f8f518e6270"
            assert result.account_id == "7a116d7d-6310-40ae-8d54-0ffbe41dc1c9"
            assert result.result['accepted'] == True
            assert result.result['reason'] == "accepted"

    def test_collections_screening_can_complete_reject(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('collections_screening/can_complete_reject')

            result = self.client.collections_screening.complete(
                "bdcca5e6-32fe-45f6-9476-6f8f518e6270",
                accepted=False,
                reason="suspected_fraud"
            )

            assert result is not None
            assert isinstance(result, CollectionsScreening)
            assert result.transaction_id == "bdcca5e6-32fe-45f6-9476-6f8f518e6270"
            assert result.result['accepted'] == False
            assert result.result['reason'] == "suspected_fraud"
