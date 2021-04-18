from django.test import TestCase

from drf_file_upload import models

FAKE_REQUEST_DOMAIN = "http://drf-file-upload.test"


class FakeRequest:
    def __init__(self, user):
        self.user = user

    def build_absolute_uri(self, url):
        return f"{FAKE_REQUEST_DOMAIN}{url}"


class BaseDrfFileUploadTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        models.AnonymousUploadedFile.objects.all().delete()
        models.AuthenticatedUploadedFile.objects.all().delete()
