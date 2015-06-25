
class Update(object):

    @classmethod
    def update_id(cls, resourceId, **params):
        return cls(**cls.post(str(resourceId), **params))

    def update(self):
        self.__class__.update_id(self['id'], self.changed_items)
        self.changed_attributes.clear()
        return self
