
class Save(object):
    def save(self):
        if not self.changed:
            return self

        self.__class__.post(self['id'], **self.changed_items)

        self.changed_attributes.clear()

        return self
