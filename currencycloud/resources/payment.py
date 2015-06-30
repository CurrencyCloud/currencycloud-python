from ..resource import Resource
from ..actions import *


class Payment(Resource, Create, Retrieve, Find, Delete, Update, Save):
    resource = "payments"
