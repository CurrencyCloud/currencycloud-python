'''This module provides the object representation of a CurrencyCloud Account'''

from .resource import Resource
from .actions import UpdateMixin

class Account(UpdateMixin, Resource):
    '''This class represents a CurrencyCloud Account'''
    pass
