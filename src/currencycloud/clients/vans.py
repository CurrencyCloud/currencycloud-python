'''This module provides a class for VANs calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Van
import deprecation


class Vans(Http):
    '''This class provides an interface to the VANs endpoints of the CC API'''

    def find(self, **kwargs):
        '''Search for VANs that meet a number of criteria and receive a paged response.'''
        response = self.get('/v2/virtual_accounts', query=kwargs)
        data = [Van(self, **fields) for fields in response['virtual_accounts']]
        return PaginatedCollection(data, response['pagination'])

    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]

    @deprecation.deprecated(deprecated_in="2.7.5", removed_in=None,
                            current_version=None,
                            details="Use the generic find function instead")
    def retrieve_subaccounts(self, resource_id, **kwargs):
        '''Get a list of VANs attached to a sub-account.'''
        response = self.get('/v2/virtual_accounts/subaccounts/' + resource_id, query=kwargs)
        data = [Van(self, **fields) for fields in response['virtual_accounts']]
        return PaginatedCollection(data, response['pagination'])

    @deprecation.deprecated(deprecated_in="2.7.5", removed_in=None,
                            current_version=None,
                            details="Use the generic find function instead")
    def find_subaccounts(self, **kwargs):
        '''Get a list of VANS for all sub-accounts.'''
        response = self.get('/v2/virtual_accounts/subaccounts/find', query=kwargs)
        data = [Van(self, **fields) for fields in response['virtual_accounts']]
        return PaginatedCollection(data, response['pagination'])
