'''This module provides a class for Funding calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, FundingAccount, PaymentChargesSettings


class Funding(Http):
    '''This class provides an interface to the Funding endpoints of the CC API'''

    def find_funding_accounts(self, **kwargs):
        '''
        Return an array containing json structures of details of the funding accounts matching the
        search criteria for the logged in user.
        '''
        response = self.get('/v2/funding_accounts/find', query=kwargs)
        data = [FundingAccount(self, **fields) for fields in response['funding_accounts']]
        return PaginatedCollection(data, response['pagination'])
