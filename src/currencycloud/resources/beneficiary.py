'''This module provides the object representation of a CurrencyCloud Beneficiary'''

from currencycloud.resources.resource import Resource
from currencycloud.resources.actions import DeleteMixin, UpdateMixin


class Beneficiary(DeleteMixin, UpdateMixin, Resource):
    '''This class represents a CurrencyCloud Beneficiary'''
    pass
