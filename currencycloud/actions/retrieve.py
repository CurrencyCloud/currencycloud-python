
class Retrieve(object):

    @classmethod
    def retrieve(cls, resourceId):
        return cls(**cls.get(resourceId))
