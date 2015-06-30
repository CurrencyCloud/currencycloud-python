from ..resource import Resource
from ..actions import *


class Contact(Resource, Create, Retrieve, Find, Update, Current, Save):
    resource = "contacts"
