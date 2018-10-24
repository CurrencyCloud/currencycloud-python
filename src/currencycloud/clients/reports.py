'''This module provides a class for Report Creating for Conversions to the CC API'''

from currencycloud.http import Http
from currencycloud.resources import Report, PaginatedCollection


class Reports(Http):
	def create_report_for_conversions(self, **kwargs):
		'''
		Creates a new conversion report and returns a hash containing the details of the new conversion report.
		'''
		return Report(self, **self.post('/v2/reports/conversions/create', kwargs))

	def find(self, **kwargs):
		'''
		Return an array containing json structures of details of the reports matching the search
		criteria for the logged in user.
		'''
		response = self.get('/v2/reports/report_requests/find', query=kwargs)
		data = [Report(self, **fields) for fields in response['report_requests']]
		return PaginatedCollection(data, response['pagination'])

	def create_report_for_payments(self, **kwargs):
		'''
		Creates a new payment report and returns a hash containing the details of the new payment report.
		'''
		return Report(self, **self.post('/v2/reports/payments/create', kwargs))

	def find_via_id(self, resource_id, **kwargs):
		'''
		Returns a json structure containing the details of the requested report.
		'''
		return Report(self, **self.get('/v2/reports/report_requests/' + resource_id, query=kwargs))
