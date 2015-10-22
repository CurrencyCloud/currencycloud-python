from contextlib import contextmanager
import threading

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
thread_storage = threading.local()


def session(authenticate=True):
    __ensure_thread_session()
    if not thread_storage.session:
        thread_storage.session = Session(
                                    environment,
                                    login_id,
                                    api_key,
                                    token,
                                    authenticate=authenticate)
    session = thread_storage.session

    if not session.authenticated and authenticate is True:
        session.authenticate()

    return session


def close_session():
    __ensure_thread_session()

    if thread_storage.session:
        thread_storage.session.close()
        thread_storage.session = None
    return True


def reset_session():
    __ensure_thread_session()
    thread_storage.session = None
    token = None


@contextmanager
def on_behalf_of(contact_id):
    from .utilities import validate_uuid4

    current_session = session()

    if current_session.on_behalf_of is not None:
        raise GeneralError('#on_behalf_of has already been set')

    if contact_id is not None and not validate_uuid4(contact_id):
        raise GeneralError('contact_id for on_behalf_of is not a valid UUID')

    current_session.on_behalf_of = contact_id
    try:
        yield
    finally:
        current_session.on_behalf_of = None


def __ensure_thread_session():
    if not hasattr(thread_storage, 'session'):
        thread_storage.session = None
