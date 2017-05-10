class Resource(object):
    def __init__(self, **data):
        self.__attributes = data

    def __dir__(self):
        return self.__attributes.keys()

    def __len__(self):
        return len(self.__attributes)

    def __iter__(self):
        return iter(self.__attributes)

    def __contains__(self, name):
        return name in self.__attributes

    def __getitem__(self, name):
        return self.__attributes[name]

    def __setitem__(self, name, value):
        self.__attributes[name] = value
        self.__changed_attributes.add(name)

    def __getattr__(self, name):
        if name.startswith('_') or name not in self.__attributes:
            return object.__getattribute__(self, name)
        return self.__getitem__(name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super(Resource, self).__setattr__(name, value)
        else:
            self.__setitem__(name, value)
