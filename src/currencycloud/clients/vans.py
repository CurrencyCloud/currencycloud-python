'''This module provides a class for VANs calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Van
import deprecation


class Vans(Http):
    '''This class provides an interface to the VANs endpoints of the CC API'''

    def find(self, **kwargs):
        '''Search for VANs that meet a number of criteria and receive a paged response.'''
        response = self.get('/v2/virtual_accounts/find', query=kwargs)
        data = [Van(self, **fields) for fields in response['virtual_accounts']]
        return PaginatedCollection(data, response['pagination'])

    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]
