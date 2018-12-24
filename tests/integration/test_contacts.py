from betamax import Betamax

from currencycloud import Client, Config
from currencycloud.resources import *


class TestContacts:
    def setup_method(self, method):
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_contacts_can_get_current(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('contacts/can_get_current')

            contact = self.client.contacts.current()
            assert contact is not None

            assert isinstance(contact, Contact)

            assert contact.login_id is not None
            assert contact.id == "16565245-1b65-464e-affa-58313192b54f"
            assert contact.first_name is not None
            assert contact.last_name is not None
            assert contact.account_id is not None
            assert contact.account_name is not None
            assert contact.status is not None
            assert contact.locale is not None
            assert contact.timezone is not None
            assert contact.email_address is not None
            assert contact.mobile_phone_number is None
            assert contact.phone_number is None
            assert contact.your_reference is None
            assert contact.date_of_birth is None
            assert contact.created_at is not None
            assert contact.updated_at is not None

    def test_actions_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('contacts/find')

            contacts = self.client.contacts.find(email_address="api.test.user2@currencycloud.com", per_page=1)

            assert contacts
            assert len(contacts) == 1

            contact = contacts[0]

            assert contact is not None
            assert isinstance(contact, Contact)

            assert contact.login_id is not None
            assert contact.id == "e54c0c4b-e6b6-4797-b471-b52fbc36a366"
            assert contact.first_name is not None
            assert contact.last_name is not None
            assert contact.account_id is not None
            assert contact.account_name is not None
            assert contact.status is not None
            assert contact.locale is not None
            assert contact.timezone is None
            assert contact.email_address == 'api.test.user2@currencycloud.com'
            assert contact.mobile_phone_number == ''
            assert contact.phone_number == '72313121212'
            assert contact.your_reference == ''
            assert contact.date_of_birth == ''
            assert contact.created_at is not None
            assert contact.updated_at is not None

    def test_actions_can_retrieve(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('contacts/retrieve')

            contact = self.client.contacts.retrieve("16565245-1b65-464e-affa-58313192b54f")

            assert contact is not None
            assert isinstance(contact, Contact)

            assert contact.login_id is not None
            assert contact.id == "16565245-1b65-464e-affa-58313192b54f"
            assert contact.first_name is not None
            assert contact.last_name is not None
            assert contact.account_id is not None
            assert contact.account_name is not None
            assert contact.status is not None
            assert contact.locale is not None
            assert contact.timezone is not None
            assert contact.email_address is not None
            assert contact.mobile_phone_number is None
            assert contact.phone_number is None
            assert contact.your_reference is None
            assert contact.date_of_birth is None
            assert contact.created_at is not None
            assert contact.updated_at is not None

    def test_contacts_can_create(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('contacts/create')

            contact = self.client.contacts.create(account_id="d0ad035e-b699-4fcd-a73c-13fb0910a884",
                                                  first_name="Test 2",
                                                  last_name="User",
                                                  email_address="api.test.user2@currencycloud.com",
                                                  phone_number="72313121212")

            assert contact is not None
            assert isinstance(contact, Contact)

            assert contact.login_id is not None
            assert contact.id is not None
            assert contact.first_name == "Test 2"
            assert contact.last_name == 'User'
            assert contact.account_id == 'd0ad035e-b699-4fcd-a73c-13fb0910a884'
            assert contact.account_name is not None
            assert contact.status is not None
            assert contact.locale is not None
            assert contact.timezone is not None
            assert contact.email_address == 'api.test.user2@currencycloud.com'
            assert contact.mobile_phone_number is None
            assert contact.phone_number == '72313121212'
            assert contact.your_reference is None
            assert contact.date_of_birth is None
            assert contact.created_at is not None
            assert contact.updated_at is not None

    def test_contacts_can_update(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('contacts/update')

            contact = self.client.contacts.retrieve("16565245-1b65-464e-affa-58313192b54f")
            assert contact is not None

            contact.login_id = "api.test.user1@currencycloud.com"
            contact.update()
            assert contact.login_id == "api.test.user1@currencycloud.com"

            contact = self.client.contacts.retrieve("16565245-1b65-464e-affa-58313192b54f")
            assert contact is not None

            assert contact.login_id == "api.test.user1@currencycloud.com"
            assert contact.id == "16565245-1b65-464e-affa-58313192b54f"
            assert contact.first_name is not None
            assert contact.last_name is not None
            assert contact.account_id is not None
            assert contact.account_name is not None
            assert contact.status is not None
            assert contact.locale is not None
            assert contact.timezone is not None
            assert contact.email_address is not None
            assert contact.mobile_phone_number is None
            assert contact.phone_number is None
            assert contact.your_reference is None
            assert contact.date_of_birth is None
            assert contact.created_at is not None
            assert contact.updated_at is not None
