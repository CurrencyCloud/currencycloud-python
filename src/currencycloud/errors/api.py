import platform
import sys
import yaml


def extract_error_code(errors):
    return errors["error_code"] if "error_code" in errors else "unknown"


def extract_error_messages(errors):
    error_messages = []
    if "error_messages" in errors and hasattr( errors["error_messages"], "items" ):
        for field, messages in errors["error_messages"].items():
            if isinstance(messages, list):
                for message in messages:
                    error_messages.append(
                        ApiError.ApiErrorMessage(
                            field,
                            message))
            else:
                error_messages.append(
                    ApiError.ApiErrorMessage(
                        field,
                        messages))
    else:
        error_messages.append(
            ApiError.ApiErrorMessage(
                "unknown",
                {"code": "unknown_error",
                 "message": "Unhandled Error occurred. Check params for details",
                 "params": errors}))
    return error_messages


REDACTED_STRING = "********"
VALUES_TO_REDACT = ["api_key"]


def redact_values(params):
    return {i: REDACTED_STRING if i in VALUES_TO_REDACT else params[i] for i in params.keys()}


class ApiError(Exception):
    class ApiErrorMessage:
        def __init__(self, field, error):
            self.field = field
            self.code = error["code"] if "code" in error else "No Code"
            self.message = error["message"] if "message" in error else "No Message"
            self.params = error["params"] if "params" in error else {}

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
            self.code = extract_error_code(errors)
            self.messages = extract_error_messages(errors)


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
                'parameters': redact_values(self.params),
                'verb': str(
                    self.verb),
                'url': self.route,
            },
            'response': {
                'status_code': self.status_code,
                'date': self.raw_response.headers['Date'],
                'request_id': self.raw_response.headers.get('x-request-id')
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
