'''This module provides the object representation of a CurrencyCloud Contact'''

from currencycloud.resources.actions import UpdateMixin
from currencycloud.resources.resource import Resource


class Contact(UpdateMixin, Resource):
    '''This class represents a CurrencyCloud Contact'''
    pass


class HMACKey(Resource):
    '''This class represents a HMAC Key for a CurrencyCloud Contact'''
    pass
