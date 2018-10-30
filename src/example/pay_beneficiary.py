'''
This is a Python implementation of the examples in https://www.currencycloud.com/developers/cookbooks/
Additional documentation for each API endpoint can be found at https://www.currencycloud.com/developers/overview.
If you have any queries or you require support, please contact our Support team at support@currencycloud.com.
'''

import currencycloud
from currencycloud.errors import ApiError
import uuid

'''
Pay a beneficiary using funds in a different currency.

In this cookbook, you will:

1. Check how much money you hold in various foreign currencies in your Currencycloud account.
2. Top up your Euros balance by trading some Pound Sterling.
3. Make a payment in Euros to a beneficiary in Germany.
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
2. Check available balances
To find out how many Euros you have, call the Get Balance endpoint, passing EUR as the third URI path parameter.
'''
try:
    balance = client.balances.for_currency('EUR')
    print("Your Euro balance is: €{0}".format(balance.amount))
except ApiError as e:
    print("Check Balance encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
You can also check the balances for all foreign currencies that you hold in your Currencycloud account by calling the
Find Balances endpoint
'''
try:
    balances = client.balances.find()
    for element in balances:
        print("Your {0} balance is {1}".format(element.currency, element.amount))
except ApiError as e:
    print("Check Balances encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
3. Top up
Check how much it will cost to buy 10,000 Euros using funds from your Pound Sterling balance, by making a call to the
Get Detailed Rates endpoint.
'''
try:
    rate = client.rates.detailed(buy_currency='GBP', sell_currency='USD', fixed_side='buy', amount=10000)
    print("To buy {0} {1} you will need to sell {2} {3}. This quote will be valid until {4}".format(rate.client_buy_amount,
                                                                                                    rate.client_buy_currency,
                                                                                                    rate.client_sell_amount,
                                                                                                    rate.client_sell_currency,
                                                                                                    rate.settlement_cut_off_time))
except ApiError as e:
    print("Detail Rate encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
If you’re happy with the quote, you may authorize the conversion by calling the Create Conversion endpoint.
'''
try:
    conversion = client.conversions.create(buy_currency='EUR',
                                           sell_currency='GBP',
                                           fixed_side='buy',
                                           amount='10000',
                                           term_agreement='true')
    print("Conversion Id {0} for {1} {2} created succesfully".format(conversion.id,
                                                                     conversion.client_buy_amount,
                                                                     conversion.buy_currency))
except ApiError as e:
    print("Conversion encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
On success, the payload of the response message will contain full details of the conversion as recorded against your
Currencycloud account. Note the unique conversion id (the id field). You’ll need this to complete the conversion.
'''

'''
4. Check payment requirements
You want to make a regular payment to a supplier based in Germany. First, check what details are required
to make a regular payment in Euros to a beneficiary with a bank account in Germany. To do that, call the
Get Beneficiary Requirements endpoint.
'''
try:
    beneficiary_details = client.reference.beneficiary_required_details(currency='EUR', bank_account_country='DE')
    print("Beneficiary required details: ", end='')
    for element in beneficiary_details[0]:
            print(element + " ", end='')
    print()
except ApiError as e:
    print("Beneficiary Details encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
The response tells us that, to make a regular payment to a German bank account in Euros, we need two pieces of
information: the IBAN and BIC/SWIFT numbers for the beneficiary. The beneficiary could be either a company or
an individual. Either way, the same information is required.
'''

'''
5. Add a beneficiary
If you know the required details, you can go ahead and create a record for the beneficiary via the
Create Beneficiary endpoint.
'''
beneficiary_id = None
try:
    beneficiary = client.beneficiaries.create(name='Acme GmbH',
                                              bank_account_holder_name='Acme GmbH',
                                              currency='EUR',
                                              beneficiary_country='DE',
                                              bank_country='DE',
                                              bic_swift='COBADEFF',
                                              iban='DE89370400440532013000')
    beneficiary_id = beneficiary.id
    print("Beneficiary Id {0} for {1}, receiving {2} in {3} created successfully".format(beneficiary_id,
                                                                                         beneficiary.name,
                                                                                         beneficiary.currency,
                                                                                         beneficiary.bank_country))
except ApiError as e:
    print("Beneficiary encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
If the beneficiary is successfully created, the response message will contain full details about the beneficiary as
recorded in your Currencycloud account. Note the beneficiary’s unique ID (id). You’ll need this to make a payment to
the beneficiary, in the next step.
'''

'''
6. Make a payment
Authorize a payment by calling the Create Payment endpoint. Optionally, you may provide an idempotency key (via the
unique_request_id parameter). This helps protect against accidental duplicate payments.
'''
try:
    payment = client.payments.create(currency='EUR',
                                     beneficiary_id=beneficiary_id,
                                     amount='10000',
                                     reason='Invoice Payment',
                                     payment_type='regular',
                                     reference='2018-014',
                                     unique_request_id=uuid.uuid4())
    print("Payment Id {0} for {1} {2} created succesfully".format(payment.id,
                                                                  payment.amount,
                                                                  payment.currency))
except ApiError as e:
    print("Payment encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

try:
    payment = client.payments.payment_confirmation('a739b199-8260-4ffa-a404-b4b58345332e')
    print(f'Payment with ID: {payment.payment_id} confirmed. ID of Confirmation: {payment.id}')
except ApiError as e:
    print("Payment encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))

'''
If the payment is successfully queued, the response payload will contain all the information about the payment as
recorded in your Currencycloud account. This does not mean that the payment was made. It just means that it is ready
for processing.

Payments are processed asynchronously. Currencycloud will process payments on the payment_date specified, provided
you hold enough money in the relevant currency at the time. It is possible to instruct payments even if you don’t hold
enough money in the relevant currency. The payments will be queued in the normal way but will not be processed until
your account balance is topped up.
'''

'''
7. Logout
It is good security practice to retire authentication tokens when they are no longer needed, rather than let them
expire. Send a request to the Logout endpoint to terminate an authentication token immediately.
'''
try:
    logoff = client.auth.close_session()
    print("Session closed")
except ApiError as e:
    print("Logout encountered an error: {0} (HTTP code {1})".format(e.code, e.status_code))
