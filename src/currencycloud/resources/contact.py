'''This module provides the object representation of a CurrencyCloud Contact'''

from currencycloud.resources.resource import Resource
from currencycloud.resources.actions import UpdateMixin


class Contact(UpdateMixin, Resource):
    '''This class represents a CurrencyCloud Contact'''
    pass
