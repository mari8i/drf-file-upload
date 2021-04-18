import os
import uuid

from django.conf import settings
from django.db import models
from django.dispatch import receiver


def get_authenticated_uploaded_file_path(instance, filename):
    ext = filename.split(".")[-1]

    # TODO: A setting for the file name too?
    filename = "%s.%s" % (uuid.uuid4(), ext)

    # TODO: Create a setting
    return os.path.join("files/", filename)


def get_anonymous_uploaded_file_path(instance, filename):
    ext = filename.split(".")[-1]

    # TODO: A setting for the file name too?
    filename = "%s.%s" % (uuid.uuid4(), ext)

    # TODO: Create a setting
    return os.path.join("uploads/", filename)


def generate_uuid():
    return str(uuid.uuid4())


class AuthenticatedUploadedFile(models.Model):
    file = models.FileField(blank=False, null=False, upload_to=get_authenticated_uploaded_file_path)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uuid = models.CharField(unique=True, max_length=64, default=None, null=True)

    def __str__(self):
        return self.file.name

    def save(self, **kwargs):
        if self.id is None:
            self.uuid = generate_uuid()
        super().save(**kwargs)

    def delete(self, *args, **kwargs):
        keep_file = kwargs.pop("keep_file", False)
        if keep_file:
            self.file = None
        return super().delete(*args, **kwargs)


class AnonymousUploadedFile(models.Model):
    file = models.FileField(blank=False, null=False, upload_to=get_anonymous_uploaded_file_path)
    uuid = models.CharField(unique=True, max_length=64)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def save(self, **kwargs):
        if self.id is None:
            self.uuid = generate_uuid()
        super().save(**kwargs)

    def delete(self, *args, **kwargs):
        keep_file = kwargs.pop("keep_file", False)
        if keep_file:
            self.file = None
        return super().delete(*args, **kwargs)


def delete_file_if_exists(file):
    if file and os.path.isfile(file.path):
        os.remove(file.path)


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
