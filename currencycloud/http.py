'''This module provides a Mixin to generate http requests to the CC API endpoints'''

import requests

class Http(object):
    '''
    Mixin for other Client classes. Provides abstract get/post methods that will add authentication
    headers when necessary and poin to the appropriate host for the environment.
    '''

    def __init__(self, config):
        self.config = config

    def get(self, endpoint, query=None, authenticated=True):
        '''Executes a GET request.'''

        url = self.__build_url(endpoint)

        if authenticated:
            headers = {'X-Auth-Token': self.config.auth_token}
        else:
            headers = {}

        response = requests.get(url, headers=headers, params=query)
        return response.json()

    def post(self, endpoint, data, authenticated=True):
        '''Executes a POST request.'''

        url = self.__build_url(endpoint)

        if authenticated:
            headers = {'X-Auth-Token': self.config.auth_token}
        else:
            headers = {}

        response = requests.post(url, headers=headers, data=data)

        return response.json()

    ENVIRONMENT_URLS = {
        'production': 'https://api.thecurrencycloud.com',
        'demo': 'https://devapi.thecurrencycloud.com',
        'uat': 'https://api-uat1.ccycloud.com',
    }

    def __build_url(self, endpoint):
        return self.__environment_url() + endpoint

    def __environment_url(self):
        return self.ENVIRONMENT_URLS[self.config.environment]
