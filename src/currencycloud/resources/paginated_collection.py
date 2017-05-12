'''This module the PaginatedCollection class'''

from currencycloud.resources.pagination import Pagination


class PaginatedCollection(list):
    '''Provides a wrapper around an array of Resources with additional pagination details'''
    def __init__(self, collection, pagination):
        super(PaginatedCollection, self).__init__(collection)
        self.__pagination = Pagination(None, **pagination)

    @property
    def pagination(self):
        '''
        Provides the pagination informations for this response, like page number and results per
        page
        '''
        return self.__pagination
