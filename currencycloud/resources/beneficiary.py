'''This module provides the object representation of a CurrencyCloud Beneficiary'''

from .resource import Resource
from .actions import UpdateMixin

class Beneficiary(UpdateMixin, Resource):
    '''This class represents a CurrencyCloud Beneficiary'''
    pass
