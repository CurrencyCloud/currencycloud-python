'''This module provides a class for Transfers calls to the CC API'''

from ..http import Http

class Transfers(Http):
    '''This class provides an interface to the Transfers endpoints of the CC API'''

    def create(self, **kwargs):
        '''
        Creates a transfer of funds from a cash manager balance of an account to the same currency
        cash manager balance of another account.
        '''
        return self.post('/v2/transfers/create', kwargs)

    def find(self, **kwargs):
        '''Returns an array of Transfer objects for the given search criteria.'''
        return self.get('/v2/transfers/find', query=kwargs)

    def retrieve(self, resource_id, **kwargs):
        '''Returns an array of Transfer objects for the given search criteria.'''
        return self.get('/v2/transfers/' + resource_id, query=kwargs)
