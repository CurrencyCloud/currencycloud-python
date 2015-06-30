import pytest
from mock import patch

import currencycloud
from currencycloud.resource import *
from currencycloud.actions import *


class TestResource:

    class Person(Resource, Save, Delete):
        resource = 'people'

    def test_resource_save_only_updates_changed_records(self):
        person = TestResource.Person(id=1, name="Alessandro", surename="Iob")

        with patch.object(TestResource.Person, 'post') as person_post:
            def post_check(url, **kargs):
                assert url == 1
                assert kargs['name'] == 'Penelope'
            person_post.side_effect = post_check

            person.name = 'Penelope'

            assert person.changed
            assert person.save() == person
            assert person.changed is False

    def test_resource_save_does_nothing_if_nothing_has_changed(self):
        person = TestResource.Person(id=1, name="Alessandro", surename="Iob")

        assert person.save() == person
        assert person.changed is False

    def test_resource_delete_removes_resource(self):
        person = TestResource.Person(id=1, name="Alessandro", surename="Iob")

        with patch.object(TestResource.Person, 'post') as person_post:
            def post_check(url, **kargs):
                assert url == '1/delete'
                return person.data

            person_post.side_effect = post_check

            assert person.delete() == person
