from rest_framework.test import APIClient

from drf_file_upload import models
from tests import serializers as test_serializers
from tests.tests import factory
from tests.tests.base_test import BaseDrfFileUploadTestCase

API_ENDPOINT = "/upload/"


class FakeRequest:
    def __init__(self, user):
        self.user = user


class AuthenticatedFileUploadTestCase(BaseDrfFileUploadTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = factory.create_user()

        self.uploaded_file = factory.create_authenticated_uploaded_file(self.user)

    def test_upload_model_serializer_valid_data(self):
        sut = self.create_serializer(self.uploaded_file.id)

        self.assertTrue(sut.is_valid())
        test_file_model = sut.save()

        self.assertIsNotNone(test_file_model, "The test model is returned")
        self.assertIsNotNone(test_file_model.file, "The test model has a file")

        self.assertFalse(
            models.AuthenticatedUploadedFile.objects.filter(id=self.uploaded_file.id).exists(),
            "Uploaded file instance is deleted on save",
        )

    def test_upload_model_serializer_invalid_data(self):
        sut = self.create_serializer(self.uploaded_file.id + 10)

        self.assertFalse(sut.is_valid())
        self.assertEqual(len(sut.errors), 1, "There is one validation error")
        self.assertTrue("file" in sut.errors, "The validation error is for the file")
        self.assertEqual(sut.errors["file"][0].code, "invalid")

    def create_serializer(self, file_id):
        sut = test_serializers.TestUserFileUploadSerializer(
            data={"file": file_id}, context={"request": FakeRequest(self.user)}
        )
        return sut
