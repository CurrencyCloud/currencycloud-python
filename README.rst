currencycloud-python
====================

|Build Status| |PyPi Status|

Currency Cloud
==============

This is the official Python SDK for v2 of Currency Cloud's API.
Additional documentation for each API endpoint can be found at
`connect.currencycloud.com <https://connect.currencycloud.com/documentation/getting-started/introduction>`__.
If you have any queries or you require support, please contact our
implementation team at implementation@currencycloud.com.

The full source code, tests and examples can be always found on
`github <https://github.com/CurrencyCloud/currencycloud-python>`__.

Installation
------------

We supports installation using standard Python “distutils” or
“setuptools” methodologies. An overview of potential setups is as
follows:

-  **Plain Python Distutis** - The library can be installed with a clean
   Python install using the services provided via Python Distutils,
   using the setup.py script.
-  **Setuptools or Distribute** - When using
   `setuptools <https://pypi.python.org/pypi/setuptools/>`__, the
   library can be installed via setup.py or easy\_install.
-  **pip** - `pip <http://pypi.python.org/pypi/pip/>`__ is an installer
   that rides on top of setuptools or distribute, replacing the usage of
   easy\_install. It is often preferred for its simpler mode of usage.

Install via pip
~~~~~~~~~~~~~~~

When pip is available, the distribution can be downloaded from PyPi and
installed in one step:

::

    pip install currencycloud

This command will download the latest released version of the library
from the Python Cheese Shop and install it to your system.

Install using setup.py
~~~~~~~~~~~~~~~~~~~~~~

Otherwise, you can install from the distribution using the setup.py
script:

::

    python setup.py install

Supported Python versions
-------------------------

This library aims to support and is `tested
against <https://travis-ci.org/CurrencyCloud/currencycloud-python>`__ the
following Ruby implementations:

-  CPython 2.6
-  CPython 2.7
-  CPython 3.2
-  CPython 3.3
-  CPython 3.4
-  pypy

Usage
=====

.. code:: python

    >>> import currencycloud

    ## Configure ##
    >>> currencycloud.login_id = '<your login id>'
    >>> currencycloud.api_key = '<your api key>'
    >>> currencycloud.environment = currencycloud.ENV_DEMOSTRATION # use currencycloud.ENV_PRODUCTION when ready

    ## Make API calls ##
    >>> currencies = currencycloud.Reference.currencies()
    >>> currencies
    [<currencycloud.resources.reference.Currency object at 0x10e6fd190>,
    <currencycloud.resources.reference.Currency object at 0x10e6fd1d0>,
    <currencycloud.resources.reference.Currency object at 0x10e6fd2d0>,
    …
    <currencycloud.resources.reference.Currency object at 0x10e6fd9d0>]

    >>> balances = currencycloud.Balance.find()
    >>> balances
    [<currencycloud.resources.balance.Balance object at 0x10e6fd7d0>]

    >>> balances.pagination
    AttrDict({u'next_page': -1, u'previous_page': -1, u'total_entries': 1, u'current_page': 1, u'total_pages': 1, u'order_asc_desc': u'asc', u'per_page': 25, u'order': u'created_at'})

    >>> balances[0].currency
    u'GBP'

    >>> currency_usd = balances[0].currency_with_code('USD')
    >>> currency_usd
    <currencycloud.resources.balance.Balance object at 0x10cddcc50>

    ## Access attributes ##
    >>> currency_usd.currency
    u'USD'

    >>> currency_usd['currency']
    u'USD'

On Behalf Of
------------

If you want to make calls on behalf of another user (e.g. someone who
has a sub-account with you), you can execute certain commands 'on behalf
of' the user's contact\_id. Here is an example:

.. code:: python

    with currencycloud.on_behalf_of('c6ece846-6df1-461d-acaa-b42a6aa74045'):
        beneficiary = currencycloud.Beneficiary.create(<params>)
        conversion = currencycloud.Conversion.create(<params>)
        payment = currencycloud.Payment.create(<params>)

Alternatively, you can just add ``on_behalf_of`` to the call parameters,
for example:

.. code:: python

    currencycloud.Account.create(account_name='My Test User', on_behalf_of='c6ece846-6df1-461d-acaa-b42a6aa74045')

Each of the above transactions will be executed in scope of the permissions
for that contact and linked to that contact. Note that the real user who
executed the transaction will also be stored.

Errors
------

When an error occurs in the API, the library aims to give us much
information as possible. Here is an example:

.. code:: yaml

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
      url: https://devapi.thecurrencycloud.com/v2/conversions/create
      verb: post
    response:
      date: Thu, 25 Jun 2015 16:46:42 GMT
      request_id: 2816384323363505615
      status_code: 400

This is split into 5 sections:

1. Error Type: In this case ``BadRequestError`` represents an HTTP 400
   error
2. Platform: The Python implementation that was used e.g. 'python -
   2.7.6'
3. Request: Details about the HTTP request that was made e.g. the POST
   parameters
4. Response: Details about the HTTP response that was returned e.g. HTTP
   status code
5. Errors: A list of errors that provide additional information

The errors section contains valuable information:

-  Field: The parameter that the error is linked to
-  Code: A code representing this error
-  Message: A human readable message that explains the error
-  Params: A hash that contains dynamic parts of the error message for
   building custom error messages

When troubleshooting API calls with Currency Cloud support, including
the full error in any correspondence can be very helpful.

Development
===========

To run the test cases we use
`tox <https://tox.readthedocs.org/en/latest/>`__, a generic virtualenv
management and test command line tool. It can be easily installed with
`pip <http://pypi.python.org/pypi/pip/>`__

::

    pip install tox

or with `setuptools <https://pypi.python.org/pypi/setuptools/>`__

::

    easy_install tox

To run the tests

::

    tox

Dependencies
------------

-  `requests <http://docs.python-requests.org/en/latest/>`__
-  `pyYAML <http://pyyaml.org/>`__
-  `attrdict <https://pypi.python.org/pypi/attrdict/2.0.0>`__

Versioning
----------

This project uses `semantic versioning <http://semver.org/>`__. You can
safely express a dependency on a major version and expect all minor and
patch versions to be backwards compatible.

Copyright
=========

Copyright (c) 2015 Currency Cloud. See `LICENSE <LICENSE.md>`__ for
details.

.. |Build Status| image:: https://travis-ci.org/CurrencyCloud/currencycloud-python.png?branch=master
   :target: https://travis-ci.org/CurrencyCloud/currencycloud-python
.. |PyPi Status| image:: https://img.shields.io/pypi/v/currencycloud.svg
    :target: https://pypi.python.org/pypi/currencycloud
