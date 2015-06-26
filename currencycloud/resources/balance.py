from ..resource import Resource
from ..actions import *

class Balance(Resource, Find):
    resource = "balances"

    @classmethod
    def currency_with_code(cls, ccy):
        return cls(**cls.get(ccy))

