'''This module provides a class for Settlements calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Settlement


class Settlements(Http):
    '''This class provides an interface to the Settlements endpoints of the CC API'''

    def add_conversion(self, resource_id, **kwargs):
        '''Add a Conversion to an open Settlement. Returns the updated Settlement object.'''
        return self.post('/v2/settlements/' + resource_id + '/add_conversion', kwargs)

    def create(self, **kwargs):
        '''Creates a new settlement and returns the settlement object.'''
        return Settlement(self, **self.post('/v2/settlements/create', kwargs))

    def delete(self, resource_id, **kwargs):
        '''Deletes an open Settlement and returns the Settlement object in its final state.'''
        return Settlement(self, **self.post('/v2/settlements/' + resource_id + '/delete', kwargs))

    def find(self, **kwargs):
        '''Returns an array of Settlement objects for the given search criteria.'''
        response = self.get('/v2/settlements/find', query=kwargs)
        data = [Settlement(self, **fields) for fields in response['settlements']]
        return PaginatedCollection(data, response['pagination'])

    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]

    def retrieve(self, resource_id, **kwargs):
        '''Returns a Settlement object for the requested ID.'''
        return Settlement(self, **self.get('/v2/settlements/' + resource_id, query=kwargs))

    def release(self, resource_id, **kwargs):
        '''Move the Settlement to state 'released', meaning it is ready to be processed.'''
        return self.post('/v2/settlements/' + resource_id + '/release', kwargs)

    def remove_conversion(self, resource_id, **kwargs):
        '''Remove a Conversion from an open Settlement. Returns the updated Settlement object.'''
        return self.post('/v2/settlements/' + resource_id + '/remove_conversion', kwargs)

    def unrelease(self, resource_id, **kwargs):
        '''
        Move the Settlement back to state 'open', allowing Conversions to be added or removed.
        '''
        return self.post('/v2/settlements/' + resource_id + '/unrelease', kwargs)
