from django.conf import settings
from django.db import models


class TestUserFileUpload(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)


class TestAnonFileUpload(models.Model):

    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)


class TestMetadataUserFileUpload(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)
    meta_size = models.PositiveBigIntegerField()
    meta_name = models.CharField(max_length=255)
