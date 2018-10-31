'''This module provides a class for Conversions calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Conversion


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

    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]

    def retrieve(self, resource_id, **kwargs):
        '''Returns a json structure containing the details of the requested conversion.'''
        return Conversion(self, **self.get('/v2/conversions/' + resource_id, query=kwargs))

    def cancel(self, resource_id, **kwargs):
        '''Returns a json structure containing the details of the conversion cancellation.'''
        return Conversion(self, **self.post('/v2/conversions/' + resource_id + '/cancel', kwargs))

    def date_change(self, resource_id, **kwargs):
        '''Returns a json structure containing the details of the conversion date change rate.'''
        return Conversion(self, **self.post('/v2/conversions/' + resource_id + '/date_change', kwargs))

    def split(self, resource_id, **kwargs):
        '''Returns a json structure containing split results as parent and child conversions.'''
        return Conversion(self, **self.post('/v2/conversions/' + resource_id + '/split', kwargs))

    def split_preview(self, resource_id, **kwargs):
        '''Returns a json structure containing split results as parent and child conversions.'''
        return Conversion(self, **self.get('/v2/conversions/' + resource_id + '/split_preview', kwargs))

    def split_history(self, resource_id, **kwargs):
        '''Returns a json structure containing split results as parent, origin and child conversions.'''
        return Conversion(self, **self.get('/v2/conversions/' + resource_id + '/split_history', kwargs))

    def date_change_quote(self, resource_id, **kwargs):
        '''
        Returns a JSON structure containing the quote for changing the date of the specified conversion.
        '''
        return Conversion(self, **self.get('/v2/conversions/' + resource_id + '/date_change_quote', kwargs))

    def cancellation_quote(self, resource_id, **kwargs):
        '''
        Returns a JSON structure containing the quote for cancelling the specified conversion.
        '''
        return Conversion(self, **self.get('/v2/conversions/' + resource_id + '/cancellation_quote', kwargs))

    def profit_and_loss(self, **kwargs):
        '''
        Return an array containing json structures of details of the conversions profit and loss matching the
        search criteria for the logged in user.
        '''
        response = self.get('/v2/conversions/profit_and_loss', query=kwargs)
        data = [Conversion(self, **fields) for fields in response['conversion_profit_and_losses']]
        return PaginatedCollection(data, response['pagination'])
