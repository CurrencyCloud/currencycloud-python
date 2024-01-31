"""This module provides the object representation of a CurrencyCloud Payment"""

from currencycloud.resources.resource import Resource
from currencycloud.resources.actions import DeleteMixin, UpdateMixin


class Payment(DeleteMixin, UpdateMixin, Resource):
    """This class represents a CurrencyCloud Payment"""
    pass


class QuotePaymentFee(Resource):
    """This class represents a quoted fee for a CurrencyCloud Payment"""
    pass


class PaymentTrackingInfo(Resource):
    """This class represents the tracking info for a CurrencyCloud Payment"""
    pass

class PaymentValidation(Resource):
    """This class represents a validation for a CurrencyCloud Payment"""
    pass
