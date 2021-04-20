import os
import uuid

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.dispatch import receiver

from drf_file_upload.settings import lib_settings


def get_authenticated_uploaded_file_path(instance, filename):
    filename_provider_class = lib_settings.AUTH_FILENAME_PROVIDER
    base_dir = lib_settings.AUTH_MEDIA_DIR

    filename_provider = filename_provider_class()
    filename = filename_provider.get_filename(filename, user=instance.user)

    return os.path.join(base_dir, filename)


def get_anonymous_uploaded_file_path(instance, filename):
    filename_provider_class = lib_settings.ANON_FILENAME_PROVIDER
    base_dir = lib_settings.ANON_MEDIA_DIR

    filename_provider = filename_provider_class()
    filename = filename_provider.get_filename(filename)

    return os.path.join(base_dir, filename)


def generate_uuid():
    return str(uuid.uuid4())


class AuthenticatedUploadedFile(models.Model):
    file = models.FileField(blank=False, null=False, upload_to=get_authenticated_uploaded_file_path)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        keep_file = kwargs.pop("keep_file", False)
        if keep_file:
            self.file = None
        return super().delete(*args, **kwargs)


class AnonymousUploadedFile(models.Model):
    file = models.FileField(blank=False, null=False, upload_to=get_anonymous_uploaded_file_path)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        keep_file = kwargs.pop("keep_file", False)
        if keep_file:
            self.file = None
        return super().delete(*args, **kwargs)


def delete_file_if_exists(file):
    if file and default_storage.exists(file.path):
        default_storage.delete(file.path)


def delete_file_on_change(model, instance):
    if not instance.pk:
        return False

    try:
        old_file = model.objects.get(pk=instance.pk).file
    except model.DoesNotExist:
        return False

    new_file = instance.file
    if old_file and old_file != new_file:
        delete_file_if_exists(old_file)


@receiver(models.signals.post_delete, sender=AuthenticatedUploadedFile)
def delete_files_on_auth_uploaded_file_delete(sender, instance, **kwargs):
    delete_file_if_exists(instance.file)


@receiver(models.signals.pre_save, sender=AuthenticatedUploadedFile)
def delete_files_on_auth_uploaded_file_change(sender, instance, **kwargs):
    delete_file_on_change(AuthenticatedUploadedFile, instance)


@receiver(models.signals.post_delete, sender=AnonymousUploadedFile)
def delete_files_on_anon_uploaded_file_delete(sender, instance, **kwargs):
    delete_file_if_exists(instance.file)


@receiver(models.signals.pre_save, sender=AnonymousUploadedFile)
def delete_files_on_anon_uploaded_file_change(sender, instance, **kwargs):
    delete_file_on_change(AnonymousUploadedFile, instance)
