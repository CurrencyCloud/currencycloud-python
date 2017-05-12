'''This module provides a Mixin to generate http requests to the CC API endpoints'''

import requests
from .config import Config


class Http(object):
    '''
    Mixin for other Client classes. Provides abstract get/post methods that will add authentication
    headers when necessary and poin to the appropriate host for the environment.
    '''

    def __init__(self, config):
        self.config = config
        self.session = requests.Session()

    def get(self, endpoint, query=None, authenticated=True):
        '''Executes a GET request.'''

        url = self.__build_url(endpoint)
        query = self.__handle_on_behalf_of(query)
        headers = self.__build_headers(authenticated)

        response = self.session.get(url, headers=headers, params=query)
        return response.json()

    def post(self, endpoint, data, authenticated=True):
        '''Executes a POST request.'''

        url = self.__build_url(endpoint)
        data = self.__handle_on_behalf_of(data)
        headers = self.__build_headers(authenticated)

        response = self.session.post(url, headers=headers, data=data)
        return response.json()

    ENVIRONMENT_URLS = {
        Config.ENV_PRODUCTION: 'https://api.thecurrencycloud.com',
        Config.ENV_DEMONSTRATION: 'https://devapi.thecurrencycloud.com',
        Config.ENV_UAT: 'https://api-uat1.ccycloud.com',
    }

    def __build_url(self, endpoint):
        return self.__environment_url() + endpoint

    def __environment_url(self):
        if self.config.environment not in self.ENVIRONMENT_URLS:
            raise RuntimeError('%s is not a valid environment name' % self.config.environment)

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
