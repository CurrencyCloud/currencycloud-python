from ..resource import Resource
from ..actions import *


class Settlement(Resource, Create, Retrieve, Find, Delete):
    resource = "settlements"

    def add_conversion(self, conversion_id):
        return self.__update_attributes(
            Settlement.add_conversion_to_settlement(
                self['id'],
                conversion_id))

    def remove_conversion(self, conversion_id):
        return self.__update_attributes(
            Settlement.remove_conversion_from_settlement(
                self['id'],
                conversion_id))

    def release(self):
        return self.__update_attributes(
            Settlement.release_settlement(
                self['id']))

    def unrelease(self):
        return self.__update_attributes(
            Settlement.unrelease_settlement(
                self['id']))

    @classmethod
    def add_conversion_to_settlement(cls, settlement_id, conversion_id):
        return cls.post(
            "{settlement_id}/add_conversion".format(settlement_id=settlement_id),  # noqa
            conversion_id=conversion_id
        )

    @classmethod
    def remove_conversion_from_settlement(cls, settlement_id, conversion_id):
        return cls.post(
            "{settlement_id}/remove_conversion".format(settlement_id=settlement_id),  # noqa
            conversion_id=conversion_id
        )

    @classmethod
    def release_settlement(cls, settlement_id):
        return cls.post(
            "{settlement_id}/release".format(settlement_id=settlement_id)
        )

    @classmethod
    def unrelease_settlement(cls, settlement_id):
        return cls.post(
            "{settlement_id}/unrelease".format(settlement_id=settlement_id)
        )

    def __update_attributes(self, settlement):
        self.conversion_ids = settlement['conversion_ids']
        self.status = settlement['status']
        self.entries = settlement['entries']
        self.updated_at = settlement['updated_at']
        self.released_at = settlement['released_at']

        return self
