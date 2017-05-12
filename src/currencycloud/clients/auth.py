'''This module provides a class for authentication related calls to the CC API'''

from currencycloud.http import Http


class Auth(Http):
    '''This class provides an interface to the Authentication endpoints of the CC API'''

    def authenticate(self):
        '''Exchange Login ID and Api Key for a temporary Auth Token'''
        return self.post('/v2/authenticate/api', {
            'login_id': self.config.login_id,
            'api_key': self.config.api_key
        }, authenticated=False, retry=False)

    def close_session(self):
        '''Invalidate the Auth Token'''
        return self.post('/v2/authenticate/close_session', {})
