from django.core import management
from django.test import TestCase

from tests.tests import factory


class TestSpectacularSchemaTestCase(TestCase):

    def setUp(self):
        self.user = factory.create_user()

    def test_spectacular_schema(self):
        management.call_command("spectacular", file="test_schema.yml")

        # TODO: Validate schema..
