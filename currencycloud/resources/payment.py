'''This module provides the object representation of a CurrencyCloud Payment'''

from .resource import Resource
from .actions import DeleteMixin, UpdateMixin

class Payment(DeleteMixin, UpdateMixin, Resource):
    '''This class represents a CurrencyCloud Payment'''
    pass
