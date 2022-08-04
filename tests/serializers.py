from rest_framework import serializers

import drf_file_upload.fields
from drf_file_upload import serializers as dfu_serializers
from tests import models as test_models


class TestUserFileUploadSerializer(dfu_serializers.UploadedFileModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = drf_file_upload.fields.UploadedFileField(required=True, allow_null=False)

    class Meta:
        model = test_models.TestUserFileUpload
        fields = ("user", "file", "created")


class TestAnonFileUploadSerializer(dfu_serializers.UploadedFileModelSerializer):

    file = drf_file_upload.fields.AnonymousUploadedFileField(required=True, allow_null=False)

    class Meta:
        model = test_models.TestAnonFileUpload
        fields = ("file", "created")


class TestUserFileMetadataUploadSerializer(dfu_serializers.UploadedFileModelSerializer):
    metadata_uploaded_files_mapping = {
        "file": [
            ("file", "file"),
            ("size", "meta_size"),
            ("name", "meta_name")
        ]
    }

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = drf_file_upload.fields.MetadataUploadedFileField(required=True, allow_null=False)
    meta_size = serializers.IntegerField(required=False, allow_null=True)
    meta_name = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = test_models.TestMetadataUserFileUpload
        fields = ("user", "file", "created", "meta_size", "meta_name")

