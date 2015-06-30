from .request_handler import RequestHandler


class Resource(object):
    resource = None
    array_fields = None

    def __init__(self, **data):
        self.__data = data
        self.__changed_attributes = set()

    # accessors

    def keys(self):
        return self.__data.keys()

    def values(self):
        return self.__data.values()

    def __len__(self):
        return self.__data.len()

    def __iter__(self):
        return iter(self.__data)

    def has_key(self, name):
        return name in self.__data

    def __contains__(self, name):
        return name in self.__data

    def get(self, key, failobj=None):
        return self.__data.get(key, failobj)

    def __getitem__(self, name):
        return self.__data[name]

    def __setitem__(self, name, value):
        self.__data[name] = value
        self.__changed_attributes.add(name)

    def __getattr__(self, name):
        if name.startswith('_') or name not in self.__data:
            return object.__getattribute__(self, name)
        return self.__getitem__(name)

    def __setattr__(self, name, value):
        if name.startswith('_') or name not in self.__data:
            super(Resource, self).__setattr__(name, value)
        else:
            self.__setitem__(name, value)

    @property
    def data(self):
        return self.__data

    @property
    def changed(self):
        return len(self.__changed_attributes) != 0

    @property
    def changed_attributes(self):
        return self.__changed_attributes

    @property
    def changed_items(self):
        items = {}
        for name in self.__changed_attributes:
            items[name] = self[name]
        return items

    # requests

    @classmethod
    def encode_parameters(cls, params):
        encoded = {}

        for k, v in params.items():
            # encode arrays like Ruby likes :(
            if cls.array_fields and k in cls.array_fields:
                k += '[]'
            encoded[k] = v

        return encoded

    @classmethod
    def get(cls, url, **params):
        return cls.request().get(
            cls.build_url(url),
            cls.encode_parameters(params))

    @classmethod
    def post(cls, url, **params):
        return cls.request().post(
            cls.build_url(url),
            cls.encode_parameters(params))

    @classmethod
    def build_url(cls, url):
        return cls.resource + "/" + str(url)

    @classmethod
    def request(cls):
        return RequestHandler()
