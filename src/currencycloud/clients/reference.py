'''This module provides a class for Reference calls to the CC API'''

from ..http import Http


class Reference(Http):
    '''This class provides an interface to the Reference endpoints of the CC API'''

    def beneficiary_required_details(self, **kwargs):
        '''Returns required beneficiary details and their basic validation formats.'''
        return self.get('/v2/reference/beneficiary_required_details', query=kwargs)

    def conversion_dates(self, **kwargs):
        '''Returns dates for which dates this currency pair can not be traded.'''
        return self.get('/v2/reference/conversion_dates', query=kwargs)

    def currencies(self):
        '''Returns a list of all the currencies that are tradeable.'''
        return self.get('/v2/reference/currencies')

    def payment_dates(self, **kwargs):
        '''
        This call returns a list of dates that are invalid when making payments of a specific
        currency.
        '''
        return self.get('/v2/reference/payment_dates', query=kwargs)

    def settlement_accounts(self, **kwargs):
        '''Returns settlement account information, detailing where funds need to be sent to.'''
        return self.get('/v2/reference/settlement_accounts', query=kwargs)
