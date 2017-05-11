'''This module provides the object representation of a CurrencyCloud Contact'''

from .resource import Resource
from .actions import UpdateMixin


class Contact(UpdateMixin, Resource):
    '''This class represents a CurrencyCloud Contact'''
    pass
