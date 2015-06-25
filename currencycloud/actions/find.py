import currencycloud
from ..resourceful_collection import ResourcefulCollection, new_class

class Find(object):

    @classmethod
    def find(cls, **params):
        response = cls.get('find', **params)
        resource_class = new_class(cls)
        return resource_class(cls.resource, cls, response)

    @classmethod
    def first(cls, **params):
        params['per_page'] = 1
        entities = cls.find(**params)

        return entities[0] if entities else None
