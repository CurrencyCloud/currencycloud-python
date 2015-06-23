__all__ = ['UnexpectedError']

from .api import ApiError
import yaml

class UnexpectedError(ApiError):
    def __init__(self, verb, route, params, inner_error):
        super(UnexpectedError, self).__init__(verb, route, params, None)

        self.inner_error = inner_error

    def __str__(self):
        class_name = self.__class__.__name__

        error_details = {
            'platform': self.platform,
            'request': {
                'parameters': self.params,
                'verb': str(self.verb),
                'url': self.route,
            },
            'inner_error': repr(self.inner_error),
        }

        return "{class_name}\n{separator}\n{dump}\n".format(
            class_name = class_name,
            separator = "---",
            dump = yaml.safe_dump(error_details, default_flow_style=False)
        )
