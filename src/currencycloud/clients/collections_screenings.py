"""This module provides a class for Collections Screening calls to the CC API"""

from currencycloud.http import Http
from currencycloud.resources import CollectionsScreening


class CollectionsScreenings(Http):
    """This class provides an interface to the Reference endpoints of the CC API"""

    def complete(self, transaction_id, **kwargs):
        return CollectionsScreening(self, **self.put('/v2/collections_screening/' + transaction_id + '/complete', kwargs))
