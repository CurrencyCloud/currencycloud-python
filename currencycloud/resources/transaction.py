from ..resource import Resource
from ..actions import *


class Transaction(Resource, Retrieve, Find):
    resource = "transactions"
