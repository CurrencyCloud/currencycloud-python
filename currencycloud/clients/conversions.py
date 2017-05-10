'''This module provides a class for Conversions calls to the CC API'''

from ..http import Http
from ..resources import PaginatedCollection, Conversion

class Conversions(Http):
    '''This class provides an interface to the Conversions endpoints of the CC API'''

    def create(self, **kwargs):
        '''Returns a json structure containing the details of the requested conversion.'''
        return Conversion(self, **self.post('/v2/conversions/create', kwargs))

    def find(self, **kwargs):
        '''
        Return an array containing json structures of details of the conversions matching the
        search criteria for the logged in user.
        '''
        response = self.get('/v2/conversions/find', query=kwargs)
        data = [Conversion(self, **fields) for fields in response['conversions']]
        return PaginatedCollection(data, response['pagination'])

    def retrieve(self, resource_id, **kwargs):
        '''Returns a json structure containing the details of the requested conversion.'''
        return Conversion(self, **self.get('/v2/conversions/' + resource_id, query=kwargs))
