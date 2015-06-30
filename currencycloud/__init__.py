from contextlib import contextmanager

from .errors import *
from .session import Session
from .version import API_VERSION
from .config import *
from .resources import *

# Configuration

environment = None
login_id = None
api_key = None
token = None

# global session management
__session = None


def session(authenticate=True):
    global __session

    if not __session:
        __session = Session(
            environment,
            login_id,
            api_key,
            token,
            authenticate=authenticate)

    if not __session.authenticated and authenticate is True:
        __session.authenticate()

    return __session


def close_session():
    global __session
    if __session:
        __session.close()
        __session = None
    return True


def reset_session():
    global __session
    __session = None
    token = None


@contextmanager
def on_behalf_of(contact_id):
    global __session
    from .utilities import validate_uuid4

    if __session.on_behalf_of is not None:
        raise GeneralError('#on_behalf_of has already been set')

    if contact_id is not None and not validate_uuid4(contact_id):
        raise GeneralError('contact_id for on_behalf_of is not a valid UUID')

    __session.on_behalf_of = contact_id
    try:
        yield
    finally:
        __session.on_behalf_of = None
