'''This module provides a class for Transactions calls to the CC API'''

from ..http import Http

class Transactions(Http):
    '''This class provides an interface to the Transactions endpoints of the CC API'''

    def find(self, **kwargs):
        '''Search for transactions that meet a number of criteria and receive a paged response.'''
        return self.get('/v2/transactions/find', query=kwargs)

    def retrieve(self, resource_id, **kwargs):
        '''Find the details of a specific transaction.'''
        return self.get('/v2/transactions/' + resource_id, query=kwargs)
