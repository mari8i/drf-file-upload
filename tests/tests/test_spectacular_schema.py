from django.core import management

from tests.tests import factory
from tests.tests.base_test import BaseDrfFileUploadTestCase


class TestSpectacularSchemaTestCase(BaseDrfFileUploadTestCase):
    def setUp(self):
        super().setUp()
        self.user = factory.create_user()

    def test_spectacular_schema(self):
        management.call_command("spectacular", file="test_schema.yml")

        # TODO: Validate schema..
