from .errors import *
from .request_handler import RequestHandler
from .config import CONFIG

import requests


class Session(object):

    def __init__(
            self,
            environment,
            login_id,
            api_key,
            token,
            authenticate=True):
        self.__requests_session = requests.Session()

        self.__environment = environment
        self.__login_id = login_id
        self.__api_key = api_key

        self.__authenticated = False

        self.on_behalf_of = None
        self.token = None

        if token:
            Session.validata_environment(environment)
            self.token = token
            self.__authenticated = True
        elif authenticate:
            self.authenticate()

    # private

    @classmethod
    def validata_environment(cls, environment):
        if environment not in CONFIG['environments']:
            raise GeneralError(
                "'{environment}' is not a valid environment, must be one of: {environments}".format(  # noqa
                    environment=environment,
                    environments=CONFIG['environments'].keys()))

    def validate(self):
        Session.validata_environment(self.environment)

        if not self.login_id:
            raise GeneralError(
                "login_id must be set using CurrencyCloud.login_id=")

        if not self.api_key:
            raise GeneralError(
                "api_key must be set using CurrencyCloud.api_key=")

    # public

    @property
    def config(self):
        return CONFIG

    @property
    def authenticated(self):
        return self.__authenticated

    @property
    def requests_session(self):
        return self.__requests_session

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
        return CONFIG['environments'][self.environment]

    def close(self):
        self.request.post('authenticate/close_session')

    def authenticate(self):
        self.validate()

        params = dict(
            login_id=self.login_id,
            api_key=self.api_key
        )

        r = self.request.post(
            'authenticate/api',
            params,
            should_retry=False,
            disable_on_behalf_of=True
        )

        self.token = r['auth_token']
        self.__authenticated = True

    def reauthenticate(self):
        self.token = None

        self.authenticate()
