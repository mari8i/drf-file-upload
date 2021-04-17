import mimetypes

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from drf_file_upload import models
from drf_file_upload.fields import AnonymousUploadedFileField, UploadedFileField


class UploadFileValidationMixin:
    def validate_file(self, value):
        if not self.is_supported_file(value.name):
            raise ValidationError("invalid-file-format")
        if not self.respects_filesize_limit(value.size):
            raise ValidationError("file-too-large")
        return value

    def is_supported_file(self, file):
        if not hasattr(settings, "DRF_FILE_UPLOAD_ALLOWED_FORMATS") or not settings.DRF_FILE_UPLOAD_ALLOWED_FORMATS:
            return True

        mimetype = mimetypes.guess_type(file)[0]
        return mimetype in settings.DRF_FILE_UPLOAD_ALLOWED_FORMATS

    def respects_filesize_limit(self, size):
        if not hasattr(settings, "DRF_FILE_UPLOAD_MAX_SIZE") or not settings.DRF_FILE_UPLOAD_MAX_SIZE:
            return True
        return size <= settings.DRF_FILE_UPLOAD_MAX_SIZE


class AuthenticatedUploadFileSerializer(UploadFileValidationMixin, serializers.ModelSerializer):
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


class AnonymousUploadFileSerializer(UploadFileValidationMixin, serializers.ModelSerializer):
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


class UploadedFileSerializerMixin:
    def clean_uploaded_files(self):
        for field_name, field_type in self.get_fields().items():
            if isinstance(field_type, AnonymousUploadedFileField) and field_name in self.validated_data:
                models.AnonymousUploadedFile.objects.filter(file=self.validated_data[field_name]).delete()
            if isinstance(field_type, UploadedFileField) and field_name in self.validated_data:
                models.AuthenticatedUploadedFile.objects.filter(file=self.validated_data[field_name]).delete()


class UploadedFileSerializer(UploadedFileSerializerMixin, serializers.Serializer):
    def save(self, **kwargs):
        self.clean_uploaded_files()
        return super().save(**kwargs)


class UploadedFileModelSerializer(UploadedFileSerializerMixin, serializers.ModelSerializer):
    def save(self, **kwargs):
        self.clean_uploaded_files()
        return super().save(**kwargs)
