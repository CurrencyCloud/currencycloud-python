from ..resource import Resource
from ..actions import *


class Beneficiary(Resource, Create, Retrieve, Find, Update, Delete, Save):
    resource = "beneficiaries"
    array_fields = ['payment_types']

    @classmethod
    def validate(cls, **params):
        return cls(**cls.post('validate', **params))
