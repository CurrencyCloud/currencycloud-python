'''This module provides the object representation of a CurrencyCloud Settlement'''

from .resource import Resource
from .actions import DeleteMixin

class Settlement(DeleteMixin, Resource):
    '''This class represents a CurrencyCloud Settlement'''
    pass
