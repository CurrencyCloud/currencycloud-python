'''This module provides the abstract Resource class'''


class Resource(object):
    '''
    An abstract CurrencyCloud resource. Maintains all the attributes and provides a common set of
    operations to all domain objects
    '''

    def __init__(self, client, **data):
        self._client = client
        self._attributes = data
        self.__changed_attributes = set()

    def __dir__(self):
        return self._attributes.keys()

    def __len__(self):
        return len(self._attributes)

    def __iter__(self):
        return iter(self._attributes)

    def __contains__(self, name):
        return name in self._attributes

    def __getitem__(self, name):
        return self._attributes[name]

    def __setitem__(self, name, value):
        self._attributes[name] = value
        self.__changed_attributes.add(name)

    def __getattr__(self, name):
        if name.startswith('_') or name not in self._attributes:
            return object.__getattribute__(self, name)
        return self.__getitem__(name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super(Resource, self).__setattr__(name, value)
        else:
            self.__setitem__(name, value)

    @property
    def changed_attributes(self):
        '''Provides the set of all attributes that have been changed since the retrieve'''
        return self.__changed_attributes

    @property
    def changed_items(self):
        '''Provides an hashmap of all attributes that have been changed since the retrieve'''
        items = {}
        for name in self.__changed_attributes:
            items[name] = self[name]

        return items
