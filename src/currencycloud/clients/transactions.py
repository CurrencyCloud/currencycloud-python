'''This module provides a class for Transactions calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Transaction


class Transactions(Http):
    '''This class provides an interface to the Transactions endpoints of the CC API'''

    def find(self, **kwargs):
        '''Search for transactions that meet a number of criteria and receive a paged response.'''
        response = self.get('/v2/transactions/find', query=kwargs)
        data = [Transaction(self, **fields) for fields in response['transactions']]
        return PaginatedCollection(data, response['pagination'])

    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]

    def retrieve(self, resource_id, **kwargs):
        '''Find the details of a specific transaction.'''
        return Transaction(self, **self.get('/v2/transactions/' + resource_id, query=kwargs))
