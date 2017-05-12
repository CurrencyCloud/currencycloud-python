'''This module provides the object representation of a CurrencyCloud Payment'''

from currencycloud.resources.resource import Resource
from currencycloud.resources.actions import DeleteMixin, UpdateMixin


class Payment(DeleteMixin, UpdateMixin, Resource):
    '''This class represents a CurrencyCloud Payment'''
    pass
