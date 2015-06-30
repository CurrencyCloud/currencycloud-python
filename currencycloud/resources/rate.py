from ..resource import Resource
from ..actions import *


class Rates(Resource):
    pass


class Rate(Resource):
    resource = "rates"

    @classmethod
    def find(cls, **params):
        response = cls.get('find', **params)

        rates = []
        for currency_pair, bid_offer in response['rates'].items():
            rate = {
                'currency_pair': currency_pair,
                'bid': bid_offer[0],
                'offer': bid_offer[1]
            }
            rates.append(cls(**rate))

        return Rates(currencies=rates, unavailable=response['unavailable'])

    @classmethod
    def detailed(cls, **params):
        return cls(**cls.get('detailed', **params))
