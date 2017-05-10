'''This module provides the object representation of a CurrencyCloud Payment'''

from .resource import Resource
from .actions import UpdateMixin

class Payment(UpdateMixin, Resource):
    '''This class represents a CurrencyCloud Payment'''
    pass
