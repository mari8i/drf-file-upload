import os
from unittest.mock import patch

from django.core import management
from django.utils import timezone

from drf_file_upload import models
from tests.tests import factory
from tests.tests.base_test import BaseDrfFileUploadTestCase


class TestDeleteExpiredUploadedFilesTestCase(BaseDrfFileUploadTestCase):
    def setUp(self):
        super().setUp()
        self.user = factory.create_user()

    def tearDown(self):
        models.AnonymousUploadedFile.objects.all().delete()
        models.AuthenticatedUploadedFile.objects.all().delete()

    def test_delete_expired_uploaded_files_deletes_expired_files(self):
        expired_date = factory.create_datetime(2021, 4, 17, 14, 2, 59)
        with patch.object(timezone, "now", return_value=expired_date):
            auth_exp_1 = factory.create_authenticated_uploaded_file(self.user)
            auth_exp_2 = factory.create_authenticated_uploaded_file(self.user)
            anon_exp_1 = factory.create_anonymous_uploaded_file()

        self.assertTrue(os.path.isfile(auth_exp_1.file.path))
        self.assertTrue(os.path.isfile(auth_exp_2.file.path))
        self.assertTrue(os.path.isfile(anon_exp_1.file.path))

        not_expired_date = factory.create_datetime(2021, 4, 17, 14, 3)
        with patch.object(timezone, "now", return_value=not_expired_date):
            auth_valid_1 = factory.create_authenticated_uploaded_file(self.user)
            auth_valid_2 = factory.create_authenticated_uploaded_file(self.user)
            anon_valid_1 = factory.create_anonymous_uploaded_file()
            anon_valid_2 = factory.create_anonymous_uploaded_file()
            anon_valid_3 = factory.create_anonymous_uploaded_file()

        cleanup_date = factory.create_datetime(2021, 4, 17, 14, 4)
        with patch.object(timezone, "now", return_value=cleanup_date):
            management.call_command("delete_expired_uploaded_files", seconds=60)

        self.assertEqual(models.AuthenticatedUploadedFile.objects.count(), 2)
        self.assertEqual(models.AnonymousUploadedFile.objects.count(), 3)

        for auth_valid in (auth_valid_1, auth_valid_2):
            self.assertTrue(models.AuthenticatedUploadedFile.objects.filter(pk=auth_valid.id).exists())

        for anon_valid in (anon_valid_1, anon_valid_2, anon_valid_3):
            self.assertTrue(models.AnonymousUploadedFile.objects.filter(pk=anon_valid.id).exists())

        self.assertFalse(os.path.exists(auth_exp_1.file.path))
        self.assertFalse(os.path.exists(auth_exp_2.file.path))
        self.assertFalse(os.path.exists(anon_exp_1.file.path))
