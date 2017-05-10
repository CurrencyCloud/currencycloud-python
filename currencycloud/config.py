'''This module provides a Client class for authentication related calls to the CC API'''

from currencycloud.clients import Auth

class Config(object):
    '''API Configuration Object. Keeps track of Credentials, Auth Token and API Environment'''

    _auth_token = None
    on_behalf_of = None

    def __init__(self, login_id, api_key, environment='demo'):
        self.login_id = login_id
        self.api_key = api_key
        self.environment = environment

        super(Config, self).__init__()

    @property
    def auth_token(self):
        '''Getter for the Auth Token. Generates one if there is None.'''
        if self._auth_token is None:
            self._auth_token = Auth(self).authenticate()['auth_token']

        return self._auth_token

    @auth_token.setter
    def auth_token(self, value):
        '''Getter for the Auth Token. Generates one if there is None.'''
        self._auth_token = value
        return self._auth_token
