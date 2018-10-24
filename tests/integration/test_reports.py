from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import *


class TestReports:
	def setup_method(self, method):
		# TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
		# login_id and api_key with valid credentials before running the tests
		login_id = 'development@currencycloud.com'
		api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
		environment = Config.ENV_DEMO
		self.client = Client(login_id, api_key, environment)

	def test_report_conversions_can_create(self):
		with Betamax(self.client.config.session) as betamax:
			betamax.use_cassette('reports/can_create_conversion_report')

			report = self.client.report.create_report_for_conversions(description='Currency Cloud Testing Environment',
																	  buy_currency='EUR',
																	  sell_currency="GBP",
																	  unique_request_id="TEST_ID")

			assert report is not None
			assert isinstance(report, Report)

			assert report.id is not None
			assert report.short_reference != 0
			assert report.status == 'processing'

	def test_report_payments_can_create(self):
		with Betamax(self.client.config.session) as betamax:
			betamax.use_cassette('reports/can_create_payment_report')

			report = self.client.report.create_report_for_payments(description='Currency Cloud Testing Environment',
																   currency='GBP',
																   amount_from='1000',
																   amount_to='10000')
			assert report is not None
			assert isinstance(report, Report)

			assert report.id is not None
			assert report.short_reference is not None
			assert report.search_params['currency'] == 'GBP'
			assert report.report_type == 'payment'
			assert report.status == 'processing'
			assert report.account_id is not None
			assert report.contact_id is not None

	def test_reports_can_find(self):
		with Betamax(self.client.config.session) as betamax:
			betamax.use_cassette('reports/can_find_reports')

			report = self.client.report.find(per_page='1')
			assert report is not None
			assert isinstance(report, PaginatedCollection)
			assert len(report) == 1
			for element in report:
				assert element.id
				assert element.short_reference is not None
				assert element.report_type is not None
				assert element.status == 'completed'
				assert element.report_url is not None
				assert element.account_id is not None
				assert element.contact_id is not None

	def test_reports_can_find_via_id(self):
		with Betamax(self.client.config.session) as betamax:
			betamax.use_cassette('reports/can_find_reports_via_id')
			report = self.client.report.find_via_id('c3ae0475-ef72-46ef-8a90-c2d3c2912911')

			assert report is not None
			assert isinstance(report, Report)

			assert report.id is not None
			assert report.short_reference is not None
			assert report.report_type is not None
			assert report.status == 'completed'
			assert report.report_url is not None
			assert report.account_id is not None
			assert report.contact_id is not None
