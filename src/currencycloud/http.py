'''This module provides a Mixin to generate http requests to the CC API endpoints'''

from currencycloud.errors import *


class Http(object):
    '''
    Mixin for other Client classes. Provides abstract get/post methods that will add authentication
    headers when necessary and poin to the appropriate host for the environment.
    '''

    def __init__(self, config):
        self.config = config
        self.session = self.config.session

    def get(self, endpoint, query=None, authenticated=True, retry=True):
        '''Executes a GET request.'''

        url = self.__build_url(endpoint)
        query = self.__encode_arrays(self.__handle_on_behalf_of(query))
        headers = self.__build_headers(authenticated)

        def execute_request(url, headers, data):
            return self.session.get(url, headers=headers, params=data)

        response = self.__handle_authentication_errors(execute_request,
                                                       retry,
                                                       url,
                                                       headers,
                                                       query,
                                                       authenticated)

        return self.__handle_errors('get', url, query, response)

    def post(self, endpoint, data, authenticated=True, retry=True):
        '''Executes a POST request.'''

        url = self.__build_url(endpoint)
        data = self.__encode_arrays(self.__handle_on_behalf_of(data))
        headers = self.__build_headers(authenticated)

        def execute_request(url, headers, data):
            return self.session.post(url, headers=headers, data=data)

        response = self.__handle_authentication_errors(execute_request,
                                                       retry,
                                                       url,
                                                       headers,
                                                       data,
                                                       authenticated)

        return self.__handle_errors('post', url, data, response)

    def __build_url(self, endpoint):
        return self.__environment_url() + endpoint

    def __environment_url(self):
        return self.config.environment_url()

    def __handle_on_behalf_of(self, data):
        if self.config.on_behalf_of is not None:
            data = {} if data is None else data

            if 'on_behalf_of' not in data:
                data['on_behalf_of'] = self.config.on_behalf_of

        return data

    def __encode_arrays(self, data):
        if data is not None:
            new_data = {}

            for k in data:
                if isinstance(data[k], list):
                    new_data[k + '[]'] = data[k]
                else:
                    new_data[k] = data[k]

            return new_data


    def __build_headers(self, authenticated):
        if authenticated:
            headers = {'X-Auth-Token': self.config.auth_token}
        else:
            headers = {}

        return headers

    HTTP_CODE_TO_ERROR = {
        400: BadRequestError,
        401: AuthenticationError,
        403: ForbiddenError,
        404: NotFoundError,
        429: TooManyRequestsError,
        500: InternalApplicationError
    }

    def __handle_errors(self, verb, url, params, response):
        if int(response.status_code / 100) == 2:
            return response.json()
        else:
            klass = Http.HTTP_CODE_TO_ERROR.get(response.status_code, ApiError)
            raise klass(verb, url, params, response)

    def __handle_authentication_errors(self, execute_request, retry, url, headers, data, authenticated):
        retry_count = 3 if retry else 1

        while retry_count:
            retry_count -= 1
            response = execute_request(url, headers, data)

            if response.status_code != 401:
                return response

            if retry:
                self.config.reauthenticate()
                headers = self.__build_headers(authenticated)

        return response
