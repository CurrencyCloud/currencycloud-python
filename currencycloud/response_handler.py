from .errors import *


class ResponseHandler(object):

    def __init__(self, verb, route, params, response):
        self.__verb = verb
        self.__route = route
        self.__params = params
        self.__response = response

    @property
    def verb(self):
        return self.__verb

    @property
    def route(self):
        return self.__route

    @property
    def params(self):
        return self.__params

    @property
    def response(self):
        return self.__response

    def process(self):
        if self.__success():
            return self.__parsed_reponse()
        else:
            self.__handle_failure()

    # private

    def __success(self):
        return self.response.status_code in (200, 202)

    def __handle_failure(self):

        error = HTTP_CODE_TO_ERROR.get(
            self.response.status_code,
            UnexpectedError)
        raise error(self.verb, self.route, self.params, self.response)

    def __parsed_reponse(self):
        return self.response.json()
