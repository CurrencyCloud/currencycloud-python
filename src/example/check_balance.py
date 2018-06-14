'''
This is a Python implementation of the examples in https://www.currencycloud.com/developers/cookbooks/
Additional documentation for each API endpoint can be found at https://www.currencycloud.com/developers/overview.
If you have any queries or you require support, please contact our Support team at support@currencycloud.com.
'''

import currencycloud
from currencycloud.errors import ApiError

'''
Checking your balances
In this cookbook, you will check how much money you hold in various foreign currencies in your Currencycloud account.
'''

'''
1. Authenticate using valid credentials.
If you do not have a valid Login ID and API Key, you can get one by registering at
https://www.currencycloud.com/developers/register-for-an-api-key/
'''
login_id = "development@currencycloud.com"
api_key = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
environment = currencycloud.Config.ENV_DEMO
client = currencycloud.Client(login_id, api_key, environment)

'''
2. Check your balance for a specific currency
To find out how many Euros you have, call the Get Balance endpoint, passing EUR as the third URI path parameter.
'''
try:
    balance = client.balances.for_currency('EUR')
    print("Your Euro balance is: €{0}".format(balance.amount))
except ApiError as e:
    print("Check Balance encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
To get a balance for any of your client sub-accounts, simply provide the sub-account UUID via the on_behalf_of query
string parameter.
'''

'''
3. Get detailed currency balances
Alternatively, the Find Balances endpoint will tell you the value of all foreign currencies that you hold in your main
Currencycloud account.
'''
try:
    balances = client.balances.find()
    for element in balances:
        print("Your {0} balance is {1}".format(element.currency, element.amount))
except ApiError as e:
    print("Detailed Balances encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
To fetch balances for any of your client sub-accounts, simply provide the sub-account UUID via the on_behalf_of query
string parameter.
'''

'''
4. Logout
It is good security practice to retire authentication tokens when they are no longer needed, rather than let them
expire. Send a request to the Logout endpoint to terminate an authentication token immediately.
'''
try:
    logoff = client.auth.close_session()
    print("Session closed")
except ApiError as e:
    print("Logout encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))
