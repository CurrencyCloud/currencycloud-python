'''This module provides a class for Accounts calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Account


class Accounts(Http):
    '''This class provides an interface to the Accounts endpoints of the CC API'''

    def create(self, **kwargs):
        '''
        Creates a new account and returns a json structure containing the details of the requested
        account.
        '''
        return Account(self, **self.post('/v2/accounts/create', kwargs))

    def current(self):
        '''Returns a json structure containing the details of the active account.'''
        return Account(self, **self.get('/v2/accounts/current'))

    def find(self, **kwargs):
        '''
        Return an array containing json structures of details of the accounts matching the
        search criteria for the logged in user.
        '''
        response = self.get('/v2/accounts/find', query=kwargs)
        data = [Account(self, **fields) for fields in response['accounts']]
        return PaginatedCollection(data, response['pagination'])

    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]

    def retrieve(self, resource_id, **kwargs):
        '''Returns a json structure containing the details of the requested account.'''
        return Account(self, **self.get('/v2/accounts/' + resource_id, query=kwargs))

    def update(self, resource_id, **kwargs):
        '''
        Updates an existing account and returns a json structure containing the details of the
        requested account.
        '''
        return Account(self, **self.post('/v2/accounts/' + resource_id, kwargs))
