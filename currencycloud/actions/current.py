
class Current(object):

    @classmethod
    def current(cls):
        return cls(**cls.get('current'))
