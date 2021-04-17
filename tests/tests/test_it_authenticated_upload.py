from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient

from drf_file_upload import models
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

    def test_file_upload_requires_logged_user(self):
        response = self.upload_file(authenticate=False)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(models.AuthenticatedUploadedFile.objects.count(), 0)

    def test_logged_user_can_upload_file(self):
        response = self.upload_file()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertTrue(response_data["id"] > 0)
        self.assertTrue(response_data["file"].startswith("http"))

        auth_uploaded_file = models.AuthenticatedUploadedFile.objects.get(id=response_data["id"])
        self.assertIsNotNone(auth_uploaded_file.file)
        self.assertEqual(auth_uploaded_file.user, self.user)

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

    def upload_file(self, filename="test_file.pdf", authenticate=True):
        if authenticate:
            self.client.force_authenticate(self.user)
        file = factory.create_simple_uploaded_file(filename=filename)
        response = self.client.post(API_ENDPOINT, {"file": file}, format="multipart")
        return response
