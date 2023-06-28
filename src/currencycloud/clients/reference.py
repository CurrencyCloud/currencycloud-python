'''This module provides a class for Reference calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import BeneficiaryRequiredDetails, ConversionDates, Currency, SettlementAccount, PayerRequiredDetails, PaymentPurposeCode, BankDetails, PaymentFeeRule


class Reference(Http):
    '''This class provides an interface to the Reference endpoints of the CC API'''

    def beneficiary_required_details(self, **kwargs):
        '''Returns required beneficiary details and their basic validation formats.'''
        response = self.get('/v2/reference/beneficiary_required_details', query=kwargs)['details']
        return [BeneficiaryRequiredDetails(self, **c) for c in response]

    def conversion_dates(self, **kwargs):
        '''Returns dates for which dates this currency pair can not be traded.'''
        return ConversionDates(self, **self.get('/v2/reference/conversion_dates', query=kwargs))

    def currencies(self):
        '''Returns a list of all the currencies that are tradeable.'''
        response = self.get('/v2/reference/currencies')['currencies']
        return [Currency(self, **c) for c in response]

    def payment_dates(self, **kwargs):
        '''
        This call returns a list of dates that are invalid when making payments of a specific
        currency.
        '''
        return self.get('/v2/reference/payment_dates', query=kwargs)

    def settlement_accounts(self, **kwargs):
        '''Returns settlement account information, detailing where funds need to be sent to.'''
        response = self.get('/v2/reference/settlement_accounts', query=kwargs)['settlement_accounts']
        return [SettlementAccount(self, **c) for c in response]

    def payer_required_details(self, **kwargs):
        '''Returns required payer details and their basic validation formats.'''
        response = self.get('/v2/reference/payer_required_details', query=kwargs)['details']
        return [PayerRequiredDetails(self, **c) for c in response]

    def payment_purpose_codes(self, **kwargs):
        '''Returns a list of valid purpose codes for the specified currency.'''
        response = self.get('/v2/reference/payment_purpose_codes', query=kwargs)['purpose_codes']
        return [PaymentPurposeCode(self, **c) for c in response]

    def bank_details(self, **kwargs):
        '''Returns the details of the bank related to the specified identifier.'''
        response = self.get('/v2/reference/bank_details', query=kwargs)
        return BankDetails(self, **response)

    def payment_fee_rules(self, **kwargs):
        '''Returns a list of payment fee rules.'''
        response = self.get('/v2/reference/payment_fee_rules', query=kwargs)['payment_fee_rules']
        return [PaymentFeeRule(self, **c) for c in response]