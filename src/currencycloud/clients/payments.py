"""This module provides a class for payments related calls to the CC API"""

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Payment, QuotePaymentFee, PaymentTrackingInfo, PaymentValidation


class Payments(Http):
    """This class provides an interface to the Payment endpoints of the CC API"""

    def create(self, sca_id: str = None, sca_token: str = None, **kwargs):
        """
        Creates a new payment and returns a hash containing the details of the created payment.

        Information that is required for your payment depends on the payment type (local or
        standard/SWIFT payment), originating country, payer country, payer legal entity type,
        beneficiary country, beneficiary entity type and payment destination country.

        For more detailed information please see our payment guide:
            http://help.currencycloud.com/world/faq/#mandatory-payment-information

        Args:
            sca_id (str): Optional - The SCA ID for the payment.
            sca_token (str): Optional - The SCA token for the payment.
            **kwargs: Additional parameters for the payment creation.
        """
        additional_headers = {}
        if sca_id:
            additional_headers["x-sca-id"] = sca_id
        if sca_token:
            additional_headers["x-sca-token"] = sca_token

        return Payment(self, **self.post('/v2/payments/create', kwargs, additional_headers=additional_headers))

    def delete(self, resource_id, **kwargs):
        """
        Delete a previously created payment and returns a hash containing the details of the
        deleted payment.
        """
        return Payment(self, **self.post('/v2/payments/' + resource_id + '/delete', kwargs))

    def find(self, **kwargs):
        """Returns an Array of Payment objects matching the search criteria."""
        response = self.get('/v2/payments/find', query=kwargs)
        data = [Payment(self, **fields) for fields in response['payments']]
        return PaginatedCollection(data, response['pagination'])

    def first(self, **params):
        params['per_page'] = 1
        return self.find(**params)[0]

    def retrieve(self, resource_id, **kwargs):
        """Returns a hash containing the details of the requested payment."""
        # Convert 'with_deleted' to lowercase
        if 'with_deleted' in kwargs and isinstance(kwargs['with_deleted'], bool):
            kwargs['with_deleted'] = str(kwargs['with_deleted']).lower()
        return Payment(self, **self.get('/v2/payments/' + resource_id, query=kwargs))

    def retrieve_submission(self, resource_id, **kwargs):
        """
        Returns a hash containing the details of MT103 information for a SWIFT submitted payment.
        """
        return self.get('/v2/payments/' + resource_id + '/submission', query=kwargs)
    
    def retrieve_submission_info(self, resource_id, **kwargs):
        """
        Retrieves new payment submission information for a payment.
        """
        return self.get(f'/v2/payments/{resource_id}/submission_info', query=kwargs)

    def update(self, resource_id, **kwargs):
        """
        Edits a previously created payment and returns a hash containing the details of the edited
        payment.

        Information that is required for your payment depends on the payment type (local or
        standard/SWIFT payment), originating country, payer country, payer legal entity type,
        beneficiary country, beneficiary entity type and payment destination country.

        For more detailed information please see our payment guide:
            http://help.currencycloud.com/world/faq/#mandatory-payment-information
        """
        return Payment(self, **self.post('/v2/payments/' + resource_id, kwargs))

    def payment_confirmation(self, resource_id, **kwargs):
        """
        Get confirmation for a payment.
        """
        return Payment(self, **self.get('/v2/payments/' + resource_id + '/confirmation', kwargs))

    def authorise(self, **kwargs):
        """
        Authorise pending payment(s) and returns a hash containing the details of the payment authorisation.
         """
        return Payment(self, **self.post('/v2/payments/authorise', kwargs))

    def payment_delivery_date(self, **kwargs):
        """
        Retrieves Payment Delivery Date.
         """
        return Payment(self, **self.get('/v2/payments/payment_delivery_date', query=kwargs))

    def quote_payment_fee(self, **kwargs):
        """
        Retrieves Quote Payment Fee.
         """
        return QuotePaymentFee(self, **self.get('/v2/payments/quote_payment_fee', query=kwargs))

    def tracking_info(self, resource_id, **kwargs):
        """
        Retrieves Payment Tracking Info.
         """
        return PaymentTrackingInfo(self, **self.get("/v2/payments/" + resource_id + "/tracking_info", query=kwargs))

    def validate(self, sca_to_authenticated_user: bool = False, **kwargs) -> PaymentValidation:
        """
        Validate Payment
        
        Args:
            sca_to_authenticated_user (bool): If True, the SCA will be sent to the authenticated user.
            **kwargs: Additional parameters for the payment validation.
        """
        additional_headers = { "x-sca-to-authenticated-user": str(sca_to_authenticated_user).lower() }
        body, headers = self.post(
            "/v2/payments/validate", 
            kwargs, 
            additional_headers=additional_headers,
            return_response_headers=True)
        result = PaymentValidation(self, **body)
        result.response_headers = headers
        return result
