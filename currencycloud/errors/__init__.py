from .general import *
from .unexpected import *
from .api import *

HTTP_CODE_TO_ERROR = {
    400: BadRequestError,
    401: AuthenticationError,
    403: ForbiddenError,
    404: NotFoundError,
    429: TooManyRequestsError,
    500: InternalApplicationError,
}

