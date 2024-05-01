from currencycloud.http import Http
from currencycloud.resources import FundingTransaction


class FundingTransactions(Http):
	'''This class provides an interface to the Funding Transaction endpoint of the CC API'''

	def get_funding_transaction(self, resource_id, **kwargs):
		'''Get the details of a specific transaction.'''
		return FundingTransaction(self, **self.get('/v2/funding_transactions/' + resource_id, kwargs))
