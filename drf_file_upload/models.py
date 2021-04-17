import os
import uuid

from django.conf import settings
from django.db import models


def get_authenticated_uploaded_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("files/", filename)


def get_anonymous_uploaded_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("uploads/", filename)


class AuthenticatedUploadedFile(models.Model):
    file = models.FileField(blank=False, null=False, upload_to=get_authenticated_uploaded_file_path)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name


class AnonymousUploadedFile(models.Model):
    file = models.FileField(blank=False, null=False, upload_to=get_anonymous_uploaded_file_path)
    uuid = models.CharField(unique=True, max_length=64)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def save(self, **kwargs):
        if self.id is None:
            self.uuid = str(uuid.uuid4())
        super().save(**kwargs)
