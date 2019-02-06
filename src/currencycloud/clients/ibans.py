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
