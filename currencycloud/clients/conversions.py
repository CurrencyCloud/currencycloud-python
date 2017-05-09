'''This module provides a class for Conversions calls to the CC API'''

from ..http import Http

class Conversions(Http):
    '''This class provides an interface to the Conversions endpoints of the CC API'''

    def create(self, **kwargs):
        '''Returns a json structure containing the details of the requested conversion.'''
        return self.post('/v2/conversions/create', kwargs)

    def find(self, **kwargs):
        '''
        Return an array containing json structures of details of the conversions matching the
        search criteria for the logged in user.
        '''
        return self.get('/v2/conversions/find', query=kwargs)

    def retrieve(self, resource_id, **kwargs):
        '''Returns a json structure containing the details of the requested conversion.'''
        return self.get('/v2/conversions/' + resource_id, query=kwargs)
