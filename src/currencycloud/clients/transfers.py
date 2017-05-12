'''This module provides a class for Transfers calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Transfer


class Transfers(Http):
    '''This class provides an interface to the Transfers endpoints of the CC API'''

    def create(self, **kwargs):
        '''
        Creates a transfer of funds from a cash manager balance of an account to the same currency
        cash manager balance of another account.
        '''
        return Transfer(self, **self.post('/v2/transfers/create', kwargs))

    def find(self, **kwargs):
        '''Returns an array of Transfer objects for the given search criteria.'''
        response = self.get('/v2/transfers/find', query=kwargs)
        data = [Transfer(self, **fields) for fields in response['transfers']]
        return PaginatedCollection(data, response['pagination'])

    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]

    def retrieve(self, resource_id, **kwargs):
        '''Returns an array of Transfer objects for the given search criteria.'''
        return Transfer(self, **self.get('/v2/transfers/' + resource_id, query=kwargs))
