'''This module provides a class for Quotes calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import Quote


class Quotes(Http):
    '''This class provides an interface to the Quotes endpoints of the CC API'''

    def create(self, **kwargs):
        '''
        Returns a json structure containing the details of the requested quote.
        Creates a new quote for the specified held-rate period.
        '''
        return Quote(self, **self.post('/v2/quotes/create', kwargs))
