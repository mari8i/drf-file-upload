from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField

from drf_file_upload import models


class AbstractUploadedFileField(serializers.Field):
    requires_context = True

    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise ValidationError("uploaded-file-invalid-uploaded-file")

        is_new_file = not data.startswith("http")

        if is_new_file:
            if len(data) != 36:
                raise ValidationError("uploaded-file-invalid-uuid")

            return self.fetch_file_or_error(data)

        # Storing the value again, without changes: This is expected to be the original URL
        raise SkipField()

    def to_representation(self, value):
        if not value:
            return None

        try:
            url = value.url
        except AttributeError:
            return None
        request = self.context.get("request", None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url

    def fetch_file_or_error(self, uuid):
        raise NotImplementedError("Must implement fetch_file_or_error")


class UploadedFileField(AbstractUploadedFileField):
    def fetch_file_or_error(self, uuid):
        user = self.context["request"].user
        try:
            file = models.AuthenticatedUploadedFile.objects.get(uuid=uuid, user=user)
            return file.file
        except models.AuthenticatedUploadedFile.DoesNotExist:
            raise ValidationError("uploaded-file-uuid-not-found")


class AnonymousUploadedFileField(AbstractUploadedFileField):
    def fetch_file_or_error(self, uuid):
        try:
            file = models.AnonymousUploadedFile.objects.get(uuid=uuid)
            return file.file
        except models.AnonymousUploadedFile.DoesNotExist:
            raise ValidationError("uploaded-file-uuid-not-found")
