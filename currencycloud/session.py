from .errors import *

from .request_handler import RequestHandler

import requests

class Session(object):

    def __init__ (self, config, environment, login_id, api_key, token, authenticate=True):
        self.__requests_session = requests.Session()

        self.__config = config
        self.__environment = environment
        self.__login_id = login_id
        self.__api_key = api_key

        self.__authenticated = False

        self.on_behalf_of = None
        self.token = None


        if token:
            self.__validata_environment(environment)
            self.token = token
            self.__authenticated = True
        elif authenticate == True:
            self.authenticate()

    # private

    def __validata_environment(self, environment):
        if environment not in self.config['environments']:
            raise GeneralError("'{environment}' is not a valid environment, must be one of: {environments}".format(
                    environment = environment,
                    environments = self.config['environments'].keys()
                ))

    def __validate(self):
        self.__validata_environment(self.environment)

        if not self.login_id:
            raise GeneralError("login_id must be set using CurrencyCloud.login_id=")

        if not self.api_key:
            raise GeneralError("api_key must be set using CurrencyCloud.api_key=")

    # public

    @property
    def authenticated(self):
        return self.__authenticated

    @property
    def requests_session(self):
        return self.__requests_session

    @property
    def config(self):
        return self.__config

    @property
    def environment(self):
        return self.__environment

    @property
    def login_id(self):
        return self.__login_id

    @property
    def api_key(self):
        return self.__api_key

    @property
    def request(self):
        return RequestHandler(self)

    def environment_url(self):
        return self.config['environments'][self.environment]

    def close(self):
        self.request.post('authenticate/close_session')

    def authenticate(self):
        self.__validate()

        params = dict(
            login_id = self.login_id,
            api_key = self.api_key
        )

        r = self.request.post(
            'authenticate/api',
            params,
            should_retry=False
        )

        self.token = r['auth_token']
        self.__authenticated = True

    def reauthenticate(self):
        self.token = None

        self.authenticate()

