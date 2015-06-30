from ..resource import Resource
from ..actions import *


class Payer(Resource, Retrieve):
    resource = "payers"
