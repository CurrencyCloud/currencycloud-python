import platform
import sys
import yaml


class ApiError(Exception):
    class ApiErrorMessage:
        def __init__(self, field, error):
            self.field = field
            self.code = error['code']
            self.message = error['message']
            self.params = error['params']

        def to_h(self):
            return {
                'field': self.field,
                'code': self.code,
                'message': self.message,
                'params': self.params,
            }

    def __init__(self, verb, route, params, response):
        super(ApiError, self).__init__()

        self.verb = verb
        self.route = route
        self.params = params

        self.raw_response = response
        self.status_code = None if response is None else response.status_code

        self.code = None
        self.messages = []

        if response is not None:
            errors = response.json()
            self.code = errors['error_code']
            self.messages = []

            for field, messages in errors['error_messages'].items():
                for message in messages:
                    self.messages.append(
                        ApiError.ApiErrorMessage(
                            field,
                            message))

    @property
    def platform(self):
        return 'python - {version} - {implementation}'.format(
            version=sys.version.split('\n')[0].strip(),
            implementation=platform.python_implementation())

    def __str__(self):
        class_name = self.__class__.__name__

        error_details = {
            'platform': self.platform,
            'request': {
                'parameters': self.params,
                'verb': str(
                    self.verb),
                'url': self.route,
            },
            'response': {
                'status_code': self.status_code,
                'date': self.raw_response.headers['Date'],
                'request_id': int(
                    self.raw_response.headers.get(
                        'x-request-id',
                        0)),
            },
            'errors': [
                m.to_h() for m in self.messages],
        }

        return "{class_name}\n{separator}\n{dump}\n".format(
            class_name=class_name,
            separator="---",
            dump=yaml.safe_dump(error_details, default_flow_style=False)
        )


class BadRequestError(ApiError):
    pass


class AuthenticationError(ApiError):
    pass


class ForbiddenError(ApiError):
    pass


class TooManyRequestsError(ApiError):
    pass


class InternalApplicationError(ApiError):
    pass


class NotFoundError(ApiError):
    pass
