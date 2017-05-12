'''This module provides the object representation of a CurrencyCloud Settlement'''

from currencycloud.resources.resource import Resource
from currencycloud.resources.actions import DeleteMixin


class Settlement(DeleteMixin, Resource):
    '''This class represents a CurrencyCloud Settlement'''

    def add_conversion(self, conversion_id):
        response = self._client.add_conversion(self.id, conversion_id=conversion_id)
        self.__update_attr(response)
        return self

    def remove_conversion(self, conversion_id):
        response = self._client.remove_conversion(self.id, conversion_id=conversion_id)
        self.__update_attr(response)
        return self

    def release(self):
        response = self._client.release(self.id)
        self.__update_attr(response)
        return self

    def unrelease(self):
        response = self._client.unrelease(self.id)
        self.__update_attr(response)
        return self

    def __update_attr(self, response):
        self.conversion_ids = response['conversion_ids']
        self.status = response['status']
        self.entries = response['entries']
        self.updated_at = response['updated_at']
        self.released_at = response['released_at']
