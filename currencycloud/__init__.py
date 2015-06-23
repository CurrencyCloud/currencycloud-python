from contextlib import contextmanager

from .errors import *
from .session import Session
from .version import API_VERSION

# Configuration

environment = None
login_id = None
api_key = None
token = None

ENV_PRODUCTION = 'production'
ENV_DEMOSTRATION = 'demonstration'
ENV_UAT = 'uat'

CONFIG = {
	'retry_count': 3,
	'environments': {
		ENV_PRODUCTION: 'https://api.thecurrencycloud.com',
		ENV_DEMOSTRATION: 'https://devapi.thecurrencycloud.com',
		ENV_UAT: 'https://api-uat1.ccycloud.com',
	}
}

# global session management
__session = None

# @mproperty
def session(authenticate=True):
	global __session

	if not __session:
		__session = Session(CONFIG, environment, login_id, api_key, token, authenticate=authenticate)

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
