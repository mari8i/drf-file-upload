import os
import re

from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient

from drf_file_upload import models
from tests.tests import factory
from tests.tests.base_test import BaseDrfFileUploadTestCase

API_ENDPOINT = "/upload/"


class AuthenticatedFileUploadTestCase(BaseDrfFileUploadTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.user = factory.create_user()

    def test_file_upload_requires_logged_user(self):
        response = self.upload_file(authenticate=False)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(models.AuthenticatedUploadedFile.objects.count(), 0)

    def test_logged_user_can_upload_file(self):
        response = self.upload_file()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertTrue("uuid" in response_data)
        self.assertTrue("file" in response_data)
        self.assertTrue(re.match(r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", response_data["uuid"]))
        self.assertTrue(response_data["file"].startswith("http"))

        auth_uploaded_file = models.AuthenticatedUploadedFile.objects.get(uuid=response_data["uuid"])
        self.assertIsNotNone(auth_uploaded_file.file)
        self.assertEqual(auth_uploaded_file.user, self.user)

        self.assertTrue(os.path.exists(auth_uploaded_file.file.path))

    def test_upload_file_max_size_returns_error_with_file_too_large(self):
        settings.DRF_FILE_UPLOAD_MAX_SIZE = 100
        response = self.upload_file()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = response.json()
        self.assertTrue("file" in error)
        self.assertEqual(error["file"], ["file-too-large"])

    def test_upload_file_max_size(self):
        settings.DRF_FILE_UPLOAD_MAX_SIZE = 100000
        response = self.upload_file()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_file_allowed_type_returns_error_with_invalid_type(self):
        settings.DRF_FILE_UPLOAD_ALLOWED_FORMATS = {"image/png", "image/jpg"}

        response = self.upload_file(filename="invalid.pdf")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = response.json()
        self.assertTrue("file" in error)
        self.assertEqual(error["file"], ["invalid-file-format"])

    def test_upload_file_allowed_type(self):
        settings.DRF_FILE_UPLOAD_ALLOWED_FORMATS = {"image/png", "image/jpg", "application/pdf"}

        response = self.upload_file(filename="valid.pdf")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_uploaded_file(self):
        self.client.force_authenticate(self.user)

        uploaded_file = factory.create_authenticated_uploaded_file(self.user)

        response = self.client.delete(f"{API_ENDPOINT}{uploaded_file.uuid}/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(os.path.exists(uploaded_file.file.path))

    def upload_file(self, filename="test_file.pdf", authenticate=True):
        if authenticate:
            self.client.force_authenticate(self.user)
        file = factory.create_simple_uploaded_file(filename=filename)
        response = self.client.post(API_ENDPOINT, {"file": file}, format="multipart")
        return response
