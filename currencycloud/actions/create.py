
class Create(object):

    @classmethod
    def create(cls, **params):
        return cls(**cls.post('create', **params))
