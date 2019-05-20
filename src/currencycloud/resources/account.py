'''This module provides the object representation of a CurrencyCloud Account'''

from currencycloud.resources.resource import Resource
from currencycloud.resources.actions import UpdateMixin


class Account(UpdateMixin, Resource):
    '''This class represents a CurrencyCloud Account'''
    pass


class PaymentChargesSettings(Resource):
    pass
