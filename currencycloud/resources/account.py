from ..resource import Resource
from ..actions import *

class Account(Resource, Create, Retrieve, Find, Update, Current):
    resource = "accounts"

