'''This module provides a class for Balances calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Balance


class Balances(Http):
    '''This class provides an interface to the Balances endpoints of the CC API'''

    def for_currency(self, currency, **kwargs):
        '''
        Provides the balance for a currency and shows the date that the balance was last updated.
        '''
        return Balance(self, **self.get('/v2/balances/' + currency, query=kwargs))

    def find(self, **kwargs):
        '''
        Search for a range of balances and receive a paged response. This is useful if you want to
        see historic balances.
        '''
        response = self.get('/v2/balances/find', query=kwargs)
        data = [Balance(self, **fields) for fields in response['balances']]
        return PaginatedCollection(data, response['pagination'])

    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]
