from django.db.models.fields.files import FieldFile
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField

from drf_file_upload.fields import UploadedFileField
from tests.tests import factory
from tests.tests.base_test import FAKE_REQUEST_DOMAIN, BaseDrfFileUploadTestCase, FakeRequest


class UploadedFileFieldTestCase(BaseDrfFileUploadTestCase):
    def setUp(self):
        super().setUp()

        self.user = factory.create_user()
        self.sut = UploadedFileField()
        self.sut._context = {"request": FakeRequest(self.user)}

    def test_to_internal_field_with_valid_uuid_returns_uploaded_file_instance(self):
        file = factory.create_authenticated_uploaded_file(self.user, "nice_pic.png")
        value = self.sut.to_internal_value(file.uuid)
        self.assertIsInstance(value, FieldFile)

    def test_to_internal_field_parameter_must_be_string(self):
        with self.assertRaises(ValidationError) as error:
            self.sut.to_internal_value(22)

        self.assertEquals(error.exception.detail[0].code, "invalid")
        self.assertEquals(str(error.exception.detail[0]), "uploaded-file-invalid-uploaded-file")

    def test_to_internal_field_parameter_must_be_valid(self):
        with self.assertRaises(ValidationError) as error:
            self.sut.to_internal_value("f" * 35)

        self.assertEquals(error.exception.detail[0].code, "invalid")
        self.assertEquals(str(error.exception.detail[0]), "uploaded-file-invalid-uuid")

        with self.assertRaises(ValidationError) as error:
            self.sut.to_internal_value("f" * 37)

        self.assertEquals(error.exception.detail[0].code, "invalid")
        self.assertEquals(str(error.exception.detail[0]), "uploaded-file-invalid-uuid")

    def test_to_internal_field_parameter_must_exist(self):
        with self.assertRaises(ValidationError) as error:
            self.sut.to_internal_value("f" * 36)

        self.assertEquals(error.exception.detail[0].code, "invalid")
        self.assertEquals(str(error.exception.detail[0]), "uploaded-file-uuid-not-found")

    def test_to_internal_skips_if_url_is_given(self):
        with self.assertRaises(SkipField):
            self.sut.to_internal_value("http://drf-upload-file.test/hello.jpg")
        with self.assertRaises(SkipField):
            self.sut.to_internal_value("https://drf-upload-file.test/hello.jpg")

    def test_to_representation(self):
        file = factory.create_authenticated_uploaded_file(self.user, "nice_pic.png")

        repr = self.sut.to_representation(file.file)
        self.assertTrue(repr.startswith(FAKE_REQUEST_DOMAIN))
        self.assertTrue(repr.endswith(".png"))
