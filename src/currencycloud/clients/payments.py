'''This module provides a class for payments related calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Payment


class Payments(Http):
    '''This class provides an interface to the Payment endpoints of the CC API'''

    def create(self, **kwargs):
        '''
        Creates a new payment and returns a hash containing the details of the created payment.

        Information that is required for your payment depends on the payment type (local or
        standard/SWIFT payment), originating country, payer country, payer legal entity type,
        beneficiary country, beneficiary entity type and payment destination country.

        For more detailed information please see our payment guide:
            http://help.currencycloud.com/world/faq/#mandatory-payment-information
        '''
        return Payment(self, **self.post('/v2/payments/create', kwargs))

    def delete(self, resource_id, **kwargs):
        '''
        Delete a prevoiusly created payment and returns a hash containing the details of the
        deleted payment.
        '''
        return Payment(self, **self.post('/v2/payments/' + resource_id + '/delete', kwargs))

    def find(self, **kwargs):
        '''Returns an Array of Payment objects matching the search criteria.'''
        response = self.get('/v2/payments/find', query=kwargs)
        data = [Payment(self, **fields) for fields in response['payments']]
        return PaginatedCollection(data, response['pagination'])

    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]

    def retrieve(self, resource_id, **kwargs):
        '''Returns a hash containing the details of the requested payment.'''
        return Payment(self, **self.get('/v2/payments/' + resource_id, query=kwargs))

    def retrieve_submission(self, resource_id, **kwargs):
        '''
        Returns a hash containing the details of MT103 information for a SWIFT submitted payment.
        '''
        return self.get('/v2/payments/' + resource_id + '/submission', query=kwargs)

    def update(self, resource_id, **kwargs):
        '''
        Edits a prevoiusly created payment and returns a hash containing the details of the edited
        payment.

        Information that is required for your payment depends on the payment type (local or
        standard/SWIFT payment), originating country, payer country, payer legal entity type,
        beneficiary country, beneficiary entity type and payment destination country.

        For more detailed information please see our payment guide:
            http://help.currencycloud.com/world/faq/#mandatory-payment-information
        '''
        return Payment(self, **self.post('/v2/payments/' + resource_id, kwargs))
