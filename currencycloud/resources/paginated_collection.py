class PaginatedCollection(list):
    def __init__(self, collection, pagination):
        super(PaginatedCollection, self).__init__(collection)
        self.__pagination = pagination

    @property
    def pagination(self):
        return self.__pagination
