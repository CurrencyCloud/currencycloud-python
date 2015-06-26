from ..resource import Resource
from ..actions import *

class Currency(Resource):
    pass

class ConversionDates(Resource):
    pass

class SettlementAccount(Resource):
    pass

class BeneficiaryRequiredDetails(Resource):
    pass

class Reference(Resource):
    resource = "reference"

    @classmethod
    def currencies(cls):
        response = cls.get("currencies")
        data = [Currency(**c) for c in response['currencies']]
        return data

    @classmethod
    def beneficiary_required_details(cls, **params):
        response = cls.get("beneficiary_required_details", **params)
        data = [BeneficiaryRequiredDetails(**c) for c in response['details']]
        return data

    @classmethod
    def conversion_dates(cls, **params):
        response = cls.get("conversion_dates", **params)
        data = ConversionDates(**response)
        return data

    @classmethod
    def settlement_accounts(cls, **params):
        response = cls.get("settlement_accounts", **params)
        data = [SettlementAccount(**d) for d in response['settlement_accounts']]
        return data
