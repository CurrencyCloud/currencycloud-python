'''This module provides a class for Transactions calls to the CC API'''

from ..http import Http
from ..resources import PaginatedCollection, Transaction

class Transactions(Http):
    '''This class provides an interface to the Transactions endpoints of the CC API'''

    def find(self, **kwargs):
        '''Search for transactions that meet a number of criteria and receive a paged response.'''
        response = self.get('/v2/transactions/find', query=kwargs)
        data = [Transaction(**fields) for fields in response['transactions']]
        return PaginatedCollection(data, response['pagination'])

    def retrieve(self, resource_id, **kwargs):
        '''Find the details of a specific transaction.'''
        return Transaction(**self.get('/v2/transactions/' + resource_id, query=kwargs))
