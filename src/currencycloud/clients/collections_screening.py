'''This module provides a class for Collections Screening calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import CollectionsScreening


class CollectionsScreeningClient(Http):
    '''This class provides an interface to the Collections Screening endpoints of the CC API'''

    def complete(self, transaction_id, **kwargs):
        '''
        Accept or reject an inbound transaction before the funds are credited to the beneficiary's account.
        '''
        return CollectionsScreening(self, **self.put('/v2/collections_screening/' + transaction_id + '/complete', kwargs))
