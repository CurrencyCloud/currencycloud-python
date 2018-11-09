'''This module provides a class for IBANs calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Iban
import deprecation


class Ibans(Http):
    '''This class provides an interface to the IBANs endpoints of the CC API'''

    def find(self, **kwargs):
        '''Search for IBANs that meet a number of criteria and receive a paged response.'''
        response = self.get('/v2/ibans/find', query=kwargs)
        data = [Iban(self, **fields) for fields in response['ibans']]
        return PaginatedCollection(data, response['pagination'])

    @deprecation.deprecated(deprecated_in="2.7.5", removed_in=None,
                            current_version=None,
                            details="Use the generic find function instead")
    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]

    @deprecation.deprecated(deprecated_in="2.7.5", removed_in=None,
                            current_version=None,
                            details="Use the generic find function instead")
    def retrieve_subaccounts(self, resource_id, **kwargs):
        '''Get a list of IBANs linked to a given sub-account.'''
        response = self.get('/v2/ibans/subaccounts/' + resource_id, query=kwargs)
        data = [Iban(self, **fields) for fields in response['ibans']]
        return PaginatedCollection(data, response['pagination'])

    @deprecation.deprecated(deprecated_in="2.7.5", removed_in=None,
                            current_version=None,
                            details="Use the generic find function instead")
    def find_subaccounts(self, **kwargs):
        '''Get a list of IBANS for all sub-accounts.'''
        response = self.get('/v2/ibans/subaccounts/find', query=kwargs)
        data = [Iban(self, **fields) for fields in response['ibans']]
        return PaginatedCollection(data, response['pagination'])
