import mimetypes

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from drf_file_upload import models
from drf_file_upload.fields import AnonymousUploadedFileField, UploadedFileField
from drf_file_upload.settings import lib_settings


class UploadFileValidationMixin:
    def validate_file(self, value):
        if not self.is_supported_file(value.name):
            raise ValidationError("invalid-file-format")
        if not self.respects_filesize_limit(value.size):
            raise ValidationError("file-too-large")
        return value

    def is_supported_file(self, file):
        allowed_formats = lib_settings.ALLOWED_FORMATS

        if not allowed_formats:
            return True

        mimetype = mimetypes.guess_type(file)[0]
        return mimetype in allowed_formats

    def respects_filesize_limit(self, size):
        max_file_size = lib_settings.MAX_FILE_SIZE
        if not max_file_size:
            return True
        return size <= max_file_size


class AuthenticatedUploadFileSerializer(UploadFileValidationMixin, serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.AuthenticatedUploadedFile
        fields = ["file", "user", "uuid", "size", "name"]
        read_only_fields = ["uuid", "user", "size", "name"]


class AnonymousUploadFileSerializer(UploadFileValidationMixin, serializers.ModelSerializer):
    class Meta:
        model = models.AnonymousUploadedFile
        fields = ["file", "uuid", "size", "name"]
        read_only_fields = ["uuid", "size", "name"]


class UploadedFileSerializerMixin:
    metadata_uploaded_files_mapping = None

    """
    Example:

    metadata_uploaded_files_mapping = {
        "file": [("file", "file"), ("size", "size"), ("name", "name")]
    }
    """

    def clean_uploaded_files(self):
        for field_name, field_type in self.get_fields().items():
            if isinstance(field_type, AnonymousUploadedFileField) and field_name in self.validated_data:
                instance = models.AnonymousUploadedFile.objects.get(file=self.validated_data[field_name])
                instance.delete(keep_file=True)
            if isinstance(field_type, UploadedFileField) and field_name in self.validated_data:
                instance = models.AuthenticatedUploadedFile.objects.get(file=self.validated_data[field_name])
                instance.delete(keep_file=True)

    def save(self, **kwargs):
        self.clean_uploaded_files()
        return super().save(**kwargs)

    def validate(self, attrs):
        if isinstance(self.metadata_uploaded_files_mapping, dict):
            self.map_metadata_file_uploads(attrs)
        return attrs

    def map_metadata_file_uploads(self, attrs):
        for mapped_field, mappings in self.metadata_uploaded_files_mapping.items():
            value = attrs.get(mapped_field)
            if value:
                for src_mapping, dst_mapping in mappings:
                    attrs[dst_mapping] = value[src_mapping]


class UploadedFileSerializer(UploadedFileSerializerMixin, serializers.Serializer):
    pass


class UploadedFileModelSerializer(UploadedFileSerializerMixin, serializers.ModelSerializer):
    pass


class UploadFileRequestSerializer(serializers.Serializer):

    file = serializers.FileField()
