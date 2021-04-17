from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField

from drf_file_upload import models


class AuthenticatedUploadFileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.AuthenticatedUploadedFile
        fields = ["file", "user", "id"]
        read_only_fields = ["id"]
        # swagger_schema_fields = {
        #     "type": openapi.TYPE_OBJECT,
        #     "title": "Upload file",
        #     "properties": {
        #         "id": openapi.Schema(title="File Id", type=openapi.TYPE_NUMBER, read_only=True),
        #         "file": openapi.Schema(
        #             title="Multipart file",
        #             type=openapi.TYPE_STRING,
        #         ),
        #     },
        # }


class AnonymousUploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnonymousUploadedFile
        fields = ["file", "uuid"]
        read_only_fields = ["uuid"]
        # swagger_schema_fields = {
        #     "type": openapi.TYPE_OBJECT,
        #     "title": "Upload file",
        #     "properties": {
        #         "uuid": openapi.Schema(title="File Unique ID", type=openapi.TYPE_STRING, read_only=True),
        #         "file": openapi.Schema(
        #             title="Multipart file",
        #             type=openapi.TYPE_STRING,
        #         ),
        #     },
        # }

    def validate_file(self, value):
        if not self._is_supported_file(value.name):
            raise ValidationError("invalid-file-format")
        if not self._respects_filesize_limit(value.size):
            raise ValidationError("file-too-large")
        return value

    def _is_supported_file(self, file):
        return True
        # mimetype = mimetypes.guess_type(file)[0]
        # return mimetype in settings.SUPPORTED_IMAGE_FORMAT or mimetype in settings.SUPPORTED_DOCUMENT_FORMAT

    def _respects_filesize_limit(self, size):
        return size <= 5242880


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


class AuthenticatedUploadedFileModelSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        for field_name, field_type in self.get_fields().items():
            if isinstance(field_type, UploadedFileField) and field_name in self.validated_data:
                models.AuthenticatedUploadedFile.objects.filter(file=self.validated_data[field_name]).delete()

        return super().save(**kwargs)


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


class UploadedRegistrationFileFieldSerializer(serializers.Serializer):

    def save(self, **kwargs):
        for field_name, field_type in self.get_fields().items():
            if isinstance(field_type, AnonymousUploadedFileField) and field_name in self.validated_data:
                models.AnonymousUploadedFile.objects.filter(file=self.validated_data[field_name]).delete()

        return super().save(**kwargs)
