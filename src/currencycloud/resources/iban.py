'''This module provides the object representation of a CurrencyCloud Contact'''

from currencycloud.resources.resource import Resource
from currencycloud.resources.actions import UpdateMixin


class Iban(UpdateMixin, Resource):
    '''This class represents a CurrencyCloud IBAN'''
    pass
