# coding=utf-8
"""
This is a Python implementation of the examples in https://www.currencycloud.com/developers/cookbooks/
Additional documentation for each API endpoint can be found at https://www.currencycloud.com/developers/overview.
If you have any queries or you require support, please contact our Support team at support@currencycloud.com.
"""

import currencycloud
from currencycloud.errors import ApiError

login_id = "development@currencycloud.com"
api_key = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
environment = currencycloud.Config.ENV_DEMO
client = currencycloud.Client(login_id, api_key, environment)

try:
	report = client.report.create_report_for_conversions(description='TEST',
														 buy_currency='EUR',
														 sell_currency="GBP",
														 unique_request_id="TEST_ID")
	print(f"Conversion report with ID: {report.id} created successfully")
except ApiError as e:
	print("Basic Exchange encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

try:
	report = client.report.create_report_for_payments(description='Tesing',
													  currency='GBP',
													  amount_from='1000',
													  amount_to='10000')
	print(f"Payment report with ID: {report.id} has been created successfully")
except ApiError as e:
	print("Basic Exchange encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

try:
	reports = client.report.find(per_page='1')
	for element in reports:
		print(f"The report with ID: {element.id} was found with URL: {element.report_url}")
		report_id = element.id
except ApiError as e:
	print("Basic Exchange encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

try:
	reports = client.report.find_via_id(report_id)
	print(f"The report with ID: {reports.id} was found with URL: {reports.report_url}")
except ApiError as e:
	print("Basic Exchange encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

try:
	logoff = client.auth.close_session()
	print("Session closed")
except ApiError as e:
	print("Logout encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))
