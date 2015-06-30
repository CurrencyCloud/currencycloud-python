import currencycloud
from .pagination import Pagination


class ResourcefulCollection(list):

    def __init__(self, resource, klass, collection):
        data = [klass(**r) for r in collection[resource]]

        super(ResourcefulCollection, self).__init__(data)

        self.__pagination = Pagination(collection['pagination'])

    @property
    def pagination(self):
        return self.__pagination


def new_class(cls):
    class_name = cls.resource.capitalize()
    if not hasattr(currencycloud, class_name):
        setattr(
            currencycloud, class_name, type(
                class_name, (ResourcefulCollection,), {}))
    resource_class = getattr(currencycloud, class_name)

    return resource_class
