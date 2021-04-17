from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField

from drf_file_upload import models


class UploadedFileField(serializers.Field):
    requires_context = True

    def to_internal_value(self, data):
        user = self.context["request"].user
        if isinstance(data, str) and data.isdigit():
            data = int(data)
        elif isinstance(data, str) and "http" not in data and data != "":
            raise ValidationError("invalid-document-id")

        if isinstance(data, int):
            try:
                file = models.AuthenticatedUploadedFile.objects.get(pk=data, user=user)
                return file.file
            except models.AuthenticatedUploadedFile.DoesNotExist:
                raise ValidationError(f"Can not find uploaded file {data} for user {user.pk}")

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


class AnonymousUploadedFileField(serializers.Field):
    requires_context = True

    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise ValidationError("invalid-uploaded-file")

        is_new_file = not data.startswith("http")
        if is_new_file:
            try:
                file = models.AnonymousUploadedFile.objects.get(uuid=data)
                return file.file
            except models.AnonymousUploadedFile.DoesNotExist:
                raise ValidationError(f"Can not find uploaded file {data}")

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
