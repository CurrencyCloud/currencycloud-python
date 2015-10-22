import sys
from threading import Thread, Event

import pytest
from mock import patch

import currencycloud
from currencycloud.session import Session
from currencycloud.request_handler import RequestHandler

class TestCurrencyCloud:

    def setup_method(self, method):
        currencycloud.environment = None
        currencycloud.login_id = None
        currencycloud.api_key = None

        currencycloud.reset_session()

    def setup_on_behalf_of(self):
        currencycloud.environment = currencycloud.ENV_DEMOSTRATION
        currencycloud.token = '4df5b3e5882a412f148dcd08fa4e5b73'
        currencycloud.session().on_behalf_of = None

    def test_environment(self):
        currencycloud.environment = "development"
        assert(currencycloud.environment == "development")

    def test_login_id(self):
        currencycloud.login_id = "test@example.com"
        assert(currencycloud.login_id == "test@example.com")

    def test_api_key(self):
        currencycloud.api_key = "e3b0d6895f91f46d9eaf5c95aa0f64dca9007b7ab0778721b6cdc0a8bc7c563b"  # noqa
        assert currencycloud.api_key == "e3b0d6895f91f46d9eaf5c95aa0f64dca9007b7ab0778721b6cdc0a8bc7c563b"  # noqa

    def test_session_returns_session_object(self):
        currencycloud.environment = currencycloud.ENV_DEMOSTRATION
        currencycloud.login_id = 'test@example.com'
        currencycloud.api_key = 'e3b0d6895f91f46d9eaf5c95aa0f64dca9007b7ab0778721b6cdc0a8bc7c563b'  # noqa

        with patch.object(RequestHandler, 'post') as request_post:
            request_post.return_value = {'auth_token': '123'}

            assert isinstance(currencycloud.session(), Session)

    def test_session_raises_error_if_environment_is_not_set(self):
        currencycloud.environment = None

        with pytest.raises(currencycloud.GeneralError) as excinfo:
            currencycloud.session()

        assert 'is not a valid environment' in str(excinfo.value)

    def test_session_raises_error_if_environment_is_not_valid(self):
        currencycloud.environment = 'invalid'

        with pytest.raises(currencycloud.GeneralError) as excinfo:
            currencycloud.session()

        assert 'is not a valid environment' in str(excinfo.value)

    def test_session_raises_error_if_login_id_is_not_set(self):
        currencycloud.environment = currencycloud.ENV_DEMOSTRATION

        with pytest.raises(currencycloud.GeneralError) as excinfo:
            currencycloud.session()

        assert 'login_id must be set' in str(excinfo.value)

    def test_session_raises_error_if_api_key_is_not_set(self):
        currencycloud.environment = currencycloud.ENV_DEMOSTRATION
        currencycloud.login_id = "test@example.com"

        with pytest.raises(currencycloud.GeneralError) as excinfo:
            currencycloud.session()

        assert 'api_key must be set' in str(excinfo.value)

    def test_session_on_behalf_of_sets_removes_value(self):
        self.setup_on_behalf_of()

        with currencycloud.on_behalf_of('c6ece846-6df1-461d-acaa-b42a6aa74045'):  # noqa
            assert currencycloud.session(
            ).on_behalf_of == 'c6ece846-6df1-461d-acaa-b42a6aa74045'

        assert currencycloud.session().on_behalf_of is None

    def test_session_on_behalf_removes_value_on_error(self):
        self.setup_on_behalf_of()

        with pytest.raises(Exception) as excinfo:
            with currencycloud.on_behalf_of('c6ece846-6df1-461d-acaa-b42a6aa74045'):  # noqa
                assert currencycloud.session(
                ).on_behalf_of == 'c6ece846-6df1-461d-acaa-b42a6aa74045'

                raise Exception('Completed Expected error')

        assert 'Completed Expected error' in str(excinfo.value)
        assert currencycloud.session().on_behalf_of is None

    def test_session_on_behalf_prevent_reentrant_usage(self):
        self.setup_on_behalf_of()

        with pytest.raises(Exception) as excinfo:
            with currencycloud.on_behalf_of('c6ece846-6df1-461d-acaa-b42a6aa74045'):  # noqa
                with currencycloud.on_behalf_of('f57b2d33-652c-4589-a8ff-7762add2706d'):  # noqa
                    raise Exception('Should raise exception')

        assert '#on_behalf_of has already been set' in str(excinfo.value)

    def test_session_on_behalf_invalid_contact_id(self):
        self.setup_on_behalf_of()

        with pytest.raises(Exception) as excinfo:
            with currencycloud.on_behalf_of('Alessandro Iob'):
                raise Exception('Should raise exception')

        assert 'contact_id for on_behalf_of is not a valid UUID' in str(
            excinfo.value)

    '''
    This test ensures that setting on_behalf_of in one thread
    doesn't get overwritten in another thread
    '''
    def test_session_on_behalf_of_threading(self):
        self.setup_on_behalf_of()

        thread2_event = Event()
        thread1_event = Event()
        testThread_event = Event()
        final_token = None
        exceptions = []

        def first_thread():
            try:
                with currencycloud.on_behalf_of('c6ece846-6df1-461d-acaa-b42a6aa74045'):
                    assert currencycloud.session().on_behalf_of == 'c6ece846-6df1-461d-acaa-b42a6aa74045'
                    thread2_event.set()
                    thread1_event.wait(5)
                    final_token = currencycloud.session().on_behalf_of
                    testThread_event.set()
            except Exception as e:
                exceptions.append("Thread 1 - " + str(e))

        def second_thread():
            try:
                thread2_event.wait()

                with currencycloud.on_behalf_of('f57b2d33-652c-4589-a8ff-7762add2706d'):
                    assert currencycloud.session().on_behalf_of == 'f57b2d33-652c-4589-a8ff-7762add2706d'
                    thread1_event.set()
            except Exception as e:
                exceptions.append("Thread 2 - " + str(e))

        threads = [Thread(target=first_thread), Thread(target=second_thread)]
        map(lambda x: x.start(), threads)
        map(lambda x: x.join(5), threads)

        thread2_event.set()
        thread1_event.set()

        assert len(exceptions) == 0
        assert currencycloud.session().on_behalf_of == final_token

