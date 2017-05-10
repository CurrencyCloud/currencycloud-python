from .resource import Resource

class Payment(Resource):
    def client(self):
        return self._client
