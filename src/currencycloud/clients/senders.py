from currencycloud.http import Http
from currencycloud.resources import Sender


class Senders(Http):
	'''This class provides an interface to the Senders endpoints of the CC API'''

	def get_sender(self, resource_id, **kwargs):
		'''Get the details of a specific sender.'''
		return Sender(self, **self.get('/v2/transactions/sender/' + resource_id, kwargs))
