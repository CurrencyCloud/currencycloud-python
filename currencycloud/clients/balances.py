'''This module provides a class for Balances calls to the CC API'''

from ..http import Http

class Balances(Http):
    '''This class provides an interface to the Balances endpoints of the CC API'''

    def for_currency(self, currency, **kwargs):
        '''
        Provides the balance for a currency and shows the date that the balance was last updated.
        '''
        return self.get('/v2/balances/' + currency, query=kwargs)

    def find(self, **kwargs):
        '''
        Search for a range of balances and receive a paged response. This is useful if you want to
        see historic balances.
        '''
        return self.get('/v2/balances/find', query=kwargs)
