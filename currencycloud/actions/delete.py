
class Delete(object):

    def delete(self):
        self.__class__.delete_id(self['id'])

        return self

    @classmethod
    def delete_id(cls, resourceId):
        return cls(
            **cls.post("{resourceId}/delete".format(resourceId=resourceId)))
