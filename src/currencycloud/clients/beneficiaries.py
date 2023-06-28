'''This module provides a class for beneficiaries calls to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Beneficiary


class Beneficiaries(Http):
    '''This class provides an interface to the Beneficiaries endpoints of the CC API'''

    def create(self, **kwargs):
        '''
        Creates a new beneficiary and returns a hash containing the details of the new beneficiary.
        Some of the optional parameters may be required depending on the requirements of the
        currency and the country.

        Please use the /v2/reference/beneficiary_required_details call to know which fields are
        required.

        Information that is required for your payment depends on the payment type (local or
        standard/SWIFT payment), originating country, payer country, payer legal entity type,
        beneficiary country, beneficiary entity type and payment destination country.

        For more detailed information please see our payment guide:
            http://help.currencycloud.com/world/faq/#mandatory-payment-information
        '''
        return Beneficiary(self, **self.post('/v2/beneficiaries/create', kwargs))

    def delete(self, resource_id, **kwargs):
        '''
        Delete a previously created beneficiary and returns a hash containing the details of the
        deleted beneficiary.
        '''
        return Beneficiary(self, **self.post('/v2/beneficiaries/' + resource_id + '/delete', kwargs))

    def find(self, **kwargs):
        '''
        Return an array containing json structures of details of the accounts matching the search
        criteria for the logged in user.
        '''
        response = self.get('/v2/beneficiaries/find', query=kwargs)
        data = [Beneficiary(self, **fields) for fields in response['beneficiaries']]
        return PaginatedCollection(data, response['pagination'])

    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]

    def retrieve(self, resource_id, **kwargs):
        '''Returns a json structure containing the details of the requested beneficiary.'''
        return Beneficiary(self, **self.get('/v2/beneficiaries/' + resource_id, query=kwargs))

    def update(self, resource_id, **kwargs):
        '''
        Updates an existing beneficiary and returns a json structure containing the details of the
        beneficiary.

        The same rules for parameters apply as for the create request.

        For more detailed information please see our payment guide:
            http://help.currencycloud.com/world/faq/#mandatory-payment-information
        '''
        return Beneficiary(self, **self.post('/v2/beneficiaries/' + resource_id, kwargs))

    def validate(self, **kwargs):
        '''
        Validates Beneficiary details without creating one. Some of the optional parameters may be
        required depending on the requirements of the currency and the country.

        Please use the /v2/reference/beneficiary_required_details call to know which fields are
        required.
        '''
        return Beneficiary(self, **self.post('/v2/beneficiaries/validate', kwargs))
