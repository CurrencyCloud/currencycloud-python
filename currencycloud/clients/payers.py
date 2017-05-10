'''This module provides a class for Payers calls to the CC API'''

from ..http import Http
from ..resources import PaginatedCollection, Payer

class Payers(Http):
    '''This class provides an interface to the Payers endpoints of the CC API'''

    def retrieve(self, resource_id, **kwargs):
        '''Returns a hash containing the details of the requested payer.'''
        return Payer(**self.get('/v2/payers/' + resource_id, query=kwargs))
