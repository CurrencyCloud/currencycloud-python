from ..resource import Resource
from ..actions import *

class Conversion(Resource, Create, Retrieve, Find):
    resource = "conversions"

