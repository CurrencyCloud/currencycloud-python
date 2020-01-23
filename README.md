# currencycloud-python
[![Build Status](https://travis-ci.org/CurrencyCloud/currencycloud-python.png?branch=master)](https://travis-ci.org/CurrencyCloud/currencycloud-python)
[![PyPi Status](https://img.shields.io/pypi/v/currency-cloud.svg)](https://pypi.python.org/pypi/currency-cloud)

# Currencycloud
This is the official Python SDK for v2 of Currencycloud's API.
Additional documentation for each API endpoint can be found at
[developer.currencycloud.com](https://developer.currencycloud.com/documentation/getting-started/introduction/).
If you have any queries or you require support, please contact our
development team at development@currencycloud.com

The full source code, tests and examples can be always found on
[github](https://github.com/CurrencyCloud/currencycloud-python).

## Installation
We support installation using standard Python "distutils" or
"setuptools" methodologies. An overview of potential setups is as
follows:
-  **pip** - [pip](http://pypi.python.org/pypi/pip/) is an installer
   that rides on top of setuptools or distribute, replacing the usage of
   easy\_install. It is often preferred for its simpler mode of usage.
-  **Plain Python Distutis** - The library can be installed with a clean
   Python install using the services provided via Python Distutils,
   using the setup.py script.
-  **Setuptools or Distribute** - When using
   [setuptools](https://pypi.python.org/pypi/setuptools/), the
   library can be installed via setup.py or easy_install.

### Install via pip
When pip is available, the distribution can be downloaded from PyPi and
installed in one step:
```
  pip install currency-cloud
```

This command will download the latest released version of the library
from the Python Cheese Shop and install it to your system.

### Install using setup.py
Otherwise, you can install from the distribution using the setup.py
script:
```
  python setup.py install
```

## Supported Python versions
This library aims to support and is [tested](https://travis-ci.org/CurrencyCloud/currencycloud-python)
under the following Python implementations:
-  CPython 2.7
-  CPython 3.4
-  CPython 3.5
-  CPython 3.6
-  CPython 3.7

## Usage
```python
>>> import currencycloud

## Configure and instantiate the Client ##
>>> login_id = '<your login id>'
>>> api_key = '<your api key>'
>>> environment = currencycloud.Config.ENV_DEMO # use currencycloud.ENV_PROD when ready
>>> client = currencycloud.Client(login_id, api_key, environment)

## Make API calls ##
>>> currencies = client.reference.currencies()
>>> currencies
[<currencycloud.resources.reference.Currency object at 0x10e6fd190>,
<currencycloud.resources.reference.Currency object at 0x10e6fd1d0>,
<currencycloud.resources.reference.Currency object at 0x10e6fd2d0>,
…
<currencycloud.resources.reference.Currency object at 0x10e6fd9d0>]

>>> balances = client.balances.find()
>>> balances
[<currencycloud.resources.balance.Balance object at 0x10e6fd7d0>]

>>> balances.pagination
<currencycloud.resources.pagination.Pagination object at 0x10b15d6a0>

>>> balances[0].currency
'GBP'

>>> currency_usd = client.balances.for_currency("USD")
>>> currency_usd
<currencycloud.resources.balance.Balance object at 0x10cddcc50>

## Access attributes ##
>>> currency_usd.currency
'USD'

>>> currency_usd['currency']
'USD'
```

### On Behalf Of
If you want to make calls on behalf of another user (e.g. someone who has a sub-account with you), you can execute certain commands 'on behalf of' the user's contact_id. Here is an example:
```python
with client.on_behalf_of('c6ece846-6df1-461d-acaa-b42a6aa74045') as new_client:
	beneficiary = new_client.beneficiaries.create(<params>)
	conversion = new_client.conversions.create(<params>)
	payment = new_client.payments.create(<params>)
```

Alternatively, you can just add ``on_behalf_of`` to the call parameters,
for example:
```python
client.accounts.create(
    account_name='My Test User',
    on_behalf_of='c6ece846-6df1-461d-acaa-b42a6aa74045'
)
```

Each of the above transactions will be executed in scope of the permissions
for that contact and linked to that contact. Note that the real user who
executed the transaction will also be stored.

### Errors
When an error occurs in the API, the library aims to give us much
information as possible. Here is an example:
```yaml
BadRequestError
---
errors:
- code: term_agreement_is_required
  field: term_agreement
  message: term_agreement is required
  params: {}
- code: term_agreement_type_is_wrong
  field: term_agreement
  message: term_agreement should be of boolean type
  params:
    type: boolean
platform: python - 2.7.6 (default, Sep  9 2014, 15:04:36) - CPython
request:
  parameters:
    amount:
      - '1000'
    buy_currency:
      - GBP
    fixed_side:
      - buy
    reason:
      - mortage
    sell_currency:
      - USD
  url: https://devapi.currencycloud.com/v2/conversions/create
  verb: post
response:
  date: Thu, 25 Jun 2017 16:46:42 GMT
  request_id: 2816384323363505615
  status_code: 400
```

This is split into 5 sections:
1. Error Type: In this case `BadRequestError` represents an HTTP 400 error
2. Platform: The Python implementation that was used e.g. 'python - 2.7.6'
3. Request: Details about the HTTP request that was made e.g. the POST parameters
4. Response: Details about the HTTP response that was returned e.g. HTTP status code
5. Errors: A list of errors that provide additional information

The errors section contains valuable information:
-  Field: The parameter that the error is linked to
-  Code: A code representing this error
-  Message: A human readable message that explains the error
-  Params: A hash that contains dynamic parts of the error message for building custom error messages

When troubleshooting API calls with Currencycloud support, including
the full error in any correspondence can be very helpful.

## Development
To manage Python environments and dependencies we use [pipenv](https://pipenv.readthedocs.org/en/latest/) and [tox](https://tox.readthedocs.org/en/latest/) to run the tests. Both can be easily installed with pip.
```
  pip install pipenv
  pip install tox
```
To run the tests:
```
  tox
```

## Dependencies
### Development
-  [requests](https://pypi.org/project/requests/)
-  [pyYAML](https://pypi.org/project/PyYAML/)
- [deprecation](https://pypi.org/project/deprecation/)

### Test
-  [pytest](https://pypi.org/project/pytest/)
-  [mock](https://pypi.org/project/mock/)
-  [requests-mock](https://pypi.org/project/requests-mock/)
-  [betamax](https://pypi.org/project/betamax/)
-  [betamax-serializers](https://pypi.org/project/betamax-serializers/)

## Contributing
**We welcome pull requests from everyone!** Please see [CONTRIBUTING](CONTRIBUTING.md)
Our sincere thanks for [helping us](HALL_OF_FAME.md) create the best API for moving money anywhere around the world!

## Versioning
This project uses [semantic versioning](http://semver.org/). You can
safely express a dependency on a major version and expect all minor and
patch versions to be backwards compatible.

## Deprecation Policy
Technology evolves quickly and we are always looking for better ways to serve our customers. From time to time we need to make room for innovation by removing sections of code that are no longer necessary. We understand this can be disruptive and consequently we have designed a Deprecation Policy that protects our customers' investment and that allows us to take advantage of modern tools, frameworks and practices in developing software.

Deprecation means that we discourage the use of a feature, design or practice because it has been superseded or is no longer considered efficient or safe but instead of removing it immediately, we mark it as **@deprecated** to provide backwards compatibility and time for you to update your projects. While the deprecated feature remains in the SDK for a period of time, we advise that you replace it with the recommended alternative which is explained in the relevant section of the code.

We remove deprecated features after **three months** from the time of announcement.

The security of our customers' assets is of paramount importance to us and sometimes we have to deprecate features because they may pose a security threat or because new, more secure, ways are available. On such occasions we reserve the right to set a different deprecation period which may range from **immediate removal** to the standard **three months**. 

Once a feature has been marked as deprecated, we no longer develop the code or implement bug fixes. We only do security fixes.

### List of features being deprecated
```
(No features are currently being deprecated)
```

# Release History
* [4.4.1] - Add funding accounts endpoint
* [4.3.7] - Update payments endpoints for payment fee parameters
* [4.1.0] - Add Bank Details endpoint
* [4.0.3] - Add Account Payment Charges Settings and Payment Delivery Date endpoints; remove deprecated VAN endpoint; update dependencies
* [3.0.1] - Minor bug fixes
* [3.0.0] - Remove deprecated functions, update unit tests, update dependencies and update copyright
* [2.7.5] - Add new Sender and Reporting endpoints; add Conversion Cancel, Conversion Split and Conversion Date Change; add Payment Submission, Payment Confirmation and Payment Authorization; fix minor bugs; deprecate obsolete endpoints and add support for Python 3.7
* [2.2.0] - Update project and dependencies to latest versions; add PayerRequiredDetails; add HTTP 403 test; update environment constants (breaking change), url and sample credentials; add Virtual Accounts and IBANs; remove unused imports
* [1.0.0] - Make the SDK thread safe

# Support
We actively support the latest version of the SDK. We support the immediate previous version on best-efforts basis. All other versions are no longer supported nor maintained.

## Copyright
Copyright (c) 2015-2019 Currencycloud. See [LICENSE](LICENSE.md) for
details.
