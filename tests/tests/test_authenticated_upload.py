from django.core.files import File
from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import APIClient

from drf_file_upload import models
from tests import serializers as test_serializers, models as test_models
from tests.tests import factory

class FakeRequest:

    def __init__(self, user):
        self.user = user

class AuthenticatedFileUploadTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = factory.create_user()

        self.request_factory = RequestFactory()

    def test_file_upload_requires_logged_user(self):
        file = factory.create_simple_uploaded_file()

        response = self.client.post("/upload/", {"file": file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(models.AuthenticatedUploadedFile.objects.count(), 0)

    def test_logged_user_can_upload_file(self):
        self.client.force_authenticate(self.user)
        file = factory.create_simple_uploaded_file()

        response = self.client.post("/upload/", {"file": file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertTrue(response_data["id"] > 0)
        self.assertTrue(response_data["file"].startswith("http"))

        auth_uploaded_file = models.AuthenticatedUploadedFile.objects.get(id=response_data["id"])
        self.assertIsNotNone(auth_uploaded_file.file)
        self.assertEqual(auth_uploaded_file.user, self.user)

    def test_upload_model_serializer(self):
        file_contents = factory.create_simple_uploaded_file()

        uploaded_file = models.AuthenticatedUploadedFile.objects.create(file=File(file_contents), user=self.user)

        sut = test_serializers.TestUserFileUploadSerializer(data={
            "file": uploaded_file.id
        }, context={
            "request": FakeRequest(self.user)
        })
        self.assertTrue(sut.is_valid())
        test_file_model = sut.save()

        self.assertIsNotNone(test_file_model)
