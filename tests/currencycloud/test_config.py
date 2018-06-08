import pytest
from mock import patch

import currencycloud

class TestConfig:
    def setup_method(self, method):
        self.client = currencycloud.Client('development@currencycloud.com', 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef', currencycloud.Config.ENV_DEMO)

    def test_environment(self):
        self.client.config.environment = 'demo'
        assert(self.client.config.environment == 'demo')

    def test_login_id(self):
        self.client.config.login_id = 'development@currencycloud.com'
        assert(self.client.config.login_id == 'development@currencycloud.com')

    def test_api_key(self):
        self.client.config.api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        assert self.client.config.api_key == 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'

    def test_session_returns_session_object(self):
        assert isinstance(self.client.config, currencycloud.Config)

    def test_session_raises_error_if_environment_is_not_set(self):
        self.client.config.environment = None

        with pytest.raises(RuntimeError) as excinfo:
            self.client.get('/any')

        assert 'is not a valid environment' in str(excinfo.value)

    def test_session_raises_error_if_environment_is_not_valid(self):
        self.client.config.environment = 'invalid'

        with pytest.raises(RuntimeError) as excinfo:
            self.client.get('/any')

        assert 'is not a valid environment' in str(excinfo.value)

    def test_session_raises_error_if_login_id_is_not_set(self):
        self.client.config.login_id = None

        with pytest.raises(RuntimeError) as excinfo:
            self.client.get('/any')

        assert 'login_id must be set' in str(excinfo.value)

    def test_session_raises_error_if_api_key_is_not_set(self):
        self.client.config.api_key = None

        with pytest.raises(RuntimeError) as excinfo:
            self.client.get('/any')

        assert 'api_key must be set' in str(excinfo.value)

    def test_session_on_behalf_of_sets_removes_value(self):
        with self.client.on_behalf_of('c6ece846-6df1-461d-acaa-b42a6aa74045') as behalf_client:
            assert behalf_client.config.on_behalf_of == 'c6ece846-6df1-461d-acaa-b42a6aa74045'

        assert self.client.config.on_behalf_of is None

    def test_session_on_behalf_invalid_contact_id(self):
        with pytest.raises(ValueError) as excinfo:
            with self.client.on_behalf_of('SomeoneElse'):
                raise Exception('Should raise exception')

        assert 'Invalid UUIDv4' in str(excinfo.value)
