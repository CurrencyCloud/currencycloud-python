from .config import *
from .payments_client import *

class Client:
    def __init__(self, login_id, api_key, environment='demo'):
        self.config = Config(login_id, api_key, environment)
