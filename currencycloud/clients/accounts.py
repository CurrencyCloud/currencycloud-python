'''This module provides a class for Accounts calls to the CC API'''

from ..http import Http

class Accounts(Http):
    '''This class provides an interface to the Accounts endpoints of the CC API'''

    def create(self, **kwargs):
        '''
        Creates a new account and returns a json structure containing the details of the requested
        account.
        '''
        return self.post('/v2/accounts/create', kwargs)

    def current(self):
        '''Returns a json structure containing the details of the active account.'''
        return self.get('/v2/accounts/current')

    def find(self, **kwargs):
        '''
        Return an array containing json structures of details of the accounts matching the
        search criteria for the logged in user.
        '''
        return self.get('/v2/accounts/find', query=kwargs)

    def retrieve(self, resource_id, **kwargs):
        '''Returns a json structure containing the details of the requested account.'''
        return self.get('/v2/accounts/' + resource_id, query=kwargs)

    def update(self, resource_id, **kwargs):
        '''
        Updates an existing account and returns a json structure containing the details of the
        requested account.
        '''
        return self.post('/v2/accounts/' + resource_id, kwargs)
