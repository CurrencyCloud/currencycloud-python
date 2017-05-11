'''This module provides a Client class for authentication related calls to the CC API'''

import clients
import uuid


class Config(object):
    '''API Configuration Object. Keeps track of Credentials, Auth Token and API Environment'''

    _auth_token = None
    _on_behalf_of = None

    ENV_PRODUCTION = 'production'
    ENV_DEMONSTRATION = 'demonstration'
    ENV_UAT = 'uat'

    def __init__(self, login_id, api_key, environment='demo'):
        self.login_id = login_id
        self.api_key = api_key
        self.environment = environment

        super(Config, self).__init__()

    @property
    def auth_token(self):
        '''Getter for the Auth Token. Generates one if there is None.'''
        if self._auth_token is None:
            if self.login_id is None:
                raise RuntimeError('login_id must be set')
            if self.api_key is None:
                raise RuntimeError('api_key must be set')

            self._auth_token = clients.Auth(self).authenticate()['auth_token']

        return self._auth_token

    @auth_token.setter
    def auth_token(self, value):
        '''Getter for the Auth Token. Generates one if there is None.'''
        self._auth_token = value
        return self._auth_token

    @property
    def on_behalf_of(self):
        '''Getter for the on_behalf_of token.'''
        return self._on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value):
        if self.__valid_uuid(value):
            self._on_behalf_of = value
            return self._on_behalf_of
        else:
            raise ValueError('Invalid UUIDv4 for on_behalf_of contact_id.')

    def __valid_uuid(self, value):
        try:
            val = uuid.UUID(value, version=4)
        except ValueError:
            return False
        return str(val) == value
