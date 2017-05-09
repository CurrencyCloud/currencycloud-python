'''This module provides a class for Contacts calls to the CC API'''

from ..http import Http

class Contacts(Http):
    '''This class provides an interface to the Contacts endpoints of the CC API'''

    def create(self, **kwargs):
        '''
        Creates a new contact which is added to the logged in account and returns a hash containing
        the details of the new contact.
        '''
        return self.post('/v2/contacts/create', kwargs)

    def current(self):
        '''
        Returns a json structure containing the details of the contact that is currently logged in.
        '''
        return self.get('/v2/contacts/current')

    def find(self, **kwargs):
        '''
        A paged response of an array containing hashes of details of the contacts matching the
        search criteria for the active user.
        '''
        return self.get('/v2/contacts/find', query=kwargs)

    def retrieve(self, resource_id, **kwargs):
        '''Returns a json structure containing the details of the requested contact.'''
        return self.get('/v2/contacts/' + resource_id, query=kwargs)

    def update(self, resource_id, **kwargs):
        '''
        Updates an existing contact and returns a hash containing the details of the requested
        contact.
        '''
        return self.post('/v2/contacts/' + resource_id, kwargs)
