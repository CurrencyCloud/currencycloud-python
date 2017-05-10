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
        query = self.__handle_on_behalf_of(query)
        headers = self.__build_headers(authenticated)

        response = requests.get(url, headers=headers, params=query)
        return response.json()

    def post(self, endpoint, data, authenticated=True):
        '''Executes a POST request.'''

        url = self.__build_url(endpoint)
        data = self.__handle_on_behalf_of(data)
        headers = self.__build_headers(authenticated)

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

    def __handle_on_behalf_of(self, data):
        if self.config.on_behalf_of is not None:
            data = {} if data is None else data

            if 'on_behalf_of' not in data:
                data['on_behalf_of'] = self.config.on_behalf_of

        return data

    def __build_headers(self, authenticated):
        if authenticated:
            headers = {'X-Auth-Token': self.config.auth_token}
        else:
            headers = {}

        return headers
