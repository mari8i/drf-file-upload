import os

from rest_framework.test import APIClient

from drf_file_upload import models
from tests import serializers as test_serializers
from tests.tests import factory
from tests.tests.base_test import BaseDrfFileUploadTestCase, FakeRequest


class AuthenticatedFileUploadTestCase(BaseDrfFileUploadTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = factory.create_user()

        self.uploaded_file = factory.create_authenticated_uploaded_file(self.user)

    def test_upload_model_serializer_valid_data(self):
        sut = self.create_serializer(self.uploaded_file.uuid)

        self.assertTrue(sut.is_valid())
        test_file_model = sut.save()

        self.assertIsNotNone(test_file_model, "The test model is returned")
        self.assertIsNotNone(test_file_model.file, "The test model has a file")

        self.assertFalse(
            models.AuthenticatedUploadedFile.objects.filter(id=self.uploaded_file.id).exists(),
            "Uploaded file instance is deleted on save",
        )

        self.assertTrue(os.path.isfile(test_file_model.file.path), "File on filesystem is preserved")

        os.remove(test_file_model.file.path)

    def test_upload_model_serializer_is_invalid_if_file_is_deleted(self):
        uuid = self.uploaded_file.uuid
        self.uploaded_file.delete()
        sut = self.create_serializer(uuid)

        self.assertFalse(sut.is_valid())
        self.assertEquals("uploaded-file-uuid-not-found", str(sut.errors["file"][0]))

    def test_upload_model_serializer_invalid_data(self):
        sut = self.create_serializer("not-a-valid-file-uuid")

        self.assertFalse(sut.is_valid())
        self.assertEqual(len(sut.errors), 1, "There is one validation error")
        self.assertTrue("file" in sut.errors, "The validation error is for the file")
        self.assertEqual(sut.errors["file"][0].code, "invalid")

    def test_upload_model_serializer_metadata_valid_data(self):
        sut = self.create_metadata_serializer(self.uploaded_file.uuid)

        self.assertTrue(sut.is_valid())
        test_file_model = sut.save()

        self.assertIsNotNone(test_file_model, "The test model is returned")
        self.assertIsNotNone(test_file_model.file, "The test model has a file")
        self.assertIsNotNone(test_file_model.meta_name, "The file name is not empty")
        self.assertIsNotNone(test_file_model.meta_size, "The file size is not empty")

        self.assertFalse(
            models.AuthenticatedUploadedFile.objects.filter(id=self.uploaded_file.id).exists(),
            "Uploaded file instance is deleted on save",
        )

        self.assertTrue(os.path.isfile(test_file_model.file.path), "File on filesystem is preserved")

        os.remove(test_file_model.file.path)

    def create_serializer(self, file_id):
        sut = test_serializers.TestUserFileUploadSerializer(
            data={"file": str(file_id)}, context={"request": FakeRequest(self.user)}
        )
        return sut

    def create_metadata_serializer(self, file_id):
        sut = test_serializers.TestUserFileMetadataUploadSerializer(
            data={"file": str(file_id)}, context={"request": FakeRequest(self.user)}
        )
        return sut
