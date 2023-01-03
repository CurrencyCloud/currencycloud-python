'''
This is a Python implementation of the examples in https://www.currencycloud.com/developers/cookbooks/
Additional documentation for each API endpoint can be found at https://www.currencycloud.com/developers/overview.
If you have any queries or you require support, please contact our Support team at support@currencycloud.com.
'''

import currencycloud
from currencycloud.errors import ApiError

'''
Convert funds from one currency to another
A conversion is a process whereby money held in one currency is traded for money in another currency. Currencycloud can
convert money into currencies of all the world’s major economies.

In this cookbook, you will:

1. Get a quote for trading Pound Sterling (GBP) for Euros (EUR).
2. Top up your Euros balance by trading some Pound Sterling.
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
2 Get a detailed quote
Check how much it will cost to buy 10,000 Euros using funds from your Pound Sterling balance, by making a call to the
Get Detailed Rates endpoint
'''
try:
    rate = client.rates.detailed(buy_currency='EUR', sell_currency='GBP', fixed_side='buy', amount=10000)
    print("To buy {0} {1} you will need to sell {2} {3}. This quote will be valid until {4}".format(rate.client_buy_amount,
                                                                                                    rate.client_buy_currency,
                                                                                                    rate.client_sell_amount,
                                                                                                    rate.client_sell_currency,
                                                                                                    rate.settlement_cut_off_time))
except ApiError as e:
    print("Detail Quote encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
On success, the response payload will contain details of Currencycloud’s quotation to make the conversion.
'''

'''
If you’re happy with the quote, you may create the conversion by calling the Create Conversion endpoint.
'''
try:
    conversion = client.conversions.create(buy_currency='EUR',
                                           sell_currency='GBP',
                                           amount='10000',
                                           fixed_side='buy',
                                           reason='Top up Euros balance',
                                           term_agreement='true')
    print("Conversion Id {0} for {1} {2} created successfully".format(conversion.id,
                                                                     conversion.client_buy_amount,
                                                                     conversion.buy_currency))
except ApiError as e:
    print("Conversion encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
On success, the payload of the response message will contain full details of the conversion as recorded against your
Currencycloud account.

This conversion will settle automatically on the settlement_date as long as there are sufficient funds in the account’s
GBP balance to cover the client_sell_amount. Please use your Cash Manager to top up your GBP balance if necessary.
'''

try:
    conversions = client.conversions.split_preview('c805aa35-9bd3-4afe-ade2-d341e551aa16', amount='100')
    print('Your conversion after successful split preview: ')
    print('Parent conversion ID: ' + conversions['parent_conversion'].get('id'))
    print('Parent conversion buy currency: ' + conversions['parent_conversion'].get('buy_currency') + " amount " + conversions['parent_conversion'].get('buy_amount'))
    print('Parent conversion sell currency: ' + conversions['parent_conversion'].get('sell_currency') + " amount " + conversions['parent_conversion'].get('sell_amount'))
    print('Child conversion buy currency: ' + conversions['child_conversion'].get('sell_currency') + " amount " + conversions['child_conversion'].get('sell_amount'))
    print('Child conversion sell currency: ' + conversions['child_conversion'].get('buy_currency') + " amount " + conversions['child_conversion'].get('buy_amount'))
except ApiError as e:
    print("Conversion encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))


try:
    conversions = client.conversions.split_history('c805aa35-9bd3-4afe-ade2-d341e551aa16')
    print('Your conversion after successful split history: ')
    for element in conversions['child_conversions']:
        print('Child conversion ID: ' + element.get('id'))
        print('Child conversion buy currency: ' + element.get('sell_currency') + " amount " + element.get('sell_amount'))
        print('Child conversion sell currency: ' + element.get('buy_currency') + " amount " + element.get('buy_amount'))

except ApiError as e:
    print("Conversion encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

try:
    change_date_quote = client.conversions.date_change_quote('2b436517-619b-4abe-a591-821dd31b264f',
                                                             new_settlement_date='2018-10-29T16:30:00+00:00')
    print(f'Data change quote for conversion with id: + {change_date_quote.conversion_id} was successful.')
    print(f'Old settlement date: {change_date_quote.old_settlement_date}')
    print(f'New settlement data: {change_date_quote.new_settlement_date}')

except ApiError as e:
    print("Conversion encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

try:
    cancellation_quote = client.conversions.cancellation_quote('63298593-bd8d-455d-8ee8-2f85dd390f2f')
    print(f'Successful Cancellation Quote,\nAmount: {cancellation_quote.amount},\nCurrency: {cancellation_quote.currency}')
except ApiError as e:
    print("Conversion encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

try:
    profit_and_loss = client.conversions.profit_and_loss()
    print('Here is all the information about profit and loss of your conversions:')
    for element in profit_and_loss:
        if float(element.amount) > 0:
            print(f'Your profit for conversion with id {element.conversion_id}, as result of {element.event_type}, '
                  f'is {element.amount} {element.currency}')
        elif float(element.amount) < 0:
            print(f'Your loss for conversion with id {element.conversion_id}, as result of {element.event_type}, is '
                  f'{element.amount} {element.currency}')
except ApiError as e:
    print("Conversion encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
3. Logout
It is good security practice to retire authentication tokens when they are no longer needed, rather than let them
expire. Send a request to the Logout endpoint to terminate an authentication token immediately.
'''
try:
    logoff = client.auth.close_session()
    print("Session closed")
except ApiError as e:
    print("Logout encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))
