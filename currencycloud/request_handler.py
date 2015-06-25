import currencycloud
from currencycloud import config

from .utilities import validate_uuid4
from .errors import *
from .response_handler import ResponseHandler

import requests
from contextlib import contextmanager

class RequestHandler(object):
    def __init__(self, session=None):
        if session is None:
            session = currencycloud.session()

        self.__session = session

    @property
    def session(self):
        return self.__session

    def build_url(self, route):
        return self.session.environment_url() + "/" + currencycloud.API_VERSION + "/" + route

    def get(self, route, params={}, **kargs):
        def callback(url, params, options):
            response = self.__session.requests_session.get(url, params=params, headers=options['headers'])
            return response

        return self.__retry_authenticate(callback, 'get', route, params, **kargs)

    def post(self, route, params={}, **kargs):
        def callback(url, params, options):
            response = self.__session.requests_session.post(url, data=params, headers=options['headers'])
            return response

        return self.__retry_authenticate(callback, 'post', route, params, **kargs)

    # private

    def __retry_authenticate(self, callback, verb, route, params, **kargs):
        try:
            should_retry = kargs.pop('should_retry', True)

            params = self.__process_params(params)
            options = self.__process_options(verb, **kargs)
            full_url = self.build_url(route)

            response = None
            retry_count = self.session.config['retry_count'] if should_retry else 1

            while retry_count:
                retry_count -= 1

                response = callback(full_url, params, options)

                # if Unauthorized than retry, otherwise stop here!
                if not should_retry or response.status_code != 401:
                    break

                self.session.reauthenticate()
                self.__refresh_options(options)

            response_handler = ResponseHandler(verb, full_url, params, response)
            return response_handler.process()
        except (ApiError, UnexpectedError) as e:
            raise
        except Exception as e:
            raise UnexpectedError(verb, full_url, params, e)

    def __process_options(self, verb, **kargs):
        options = {'headers': self.__headers()}
        options.update(kargs)

        return options

    def __refresh_options(self, options):
        options['headers'].update(self.__headers())
        return options

    def __process_params(self, params):
        if self.session and self.session.on_behalf_of and validate_uuid4(self.session.on_behalf_of):
            params['on_behalf_of'] = self.session.on_behalf_of

        return params

    def __headers(self):
        headers = {}

        if self.session and self.session.token:
            headers['X-Auth-Token'] = self.session.token

        return headers

