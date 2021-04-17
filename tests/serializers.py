from rest_framework import serializers

from drf_file_upload import serializers as dfu_serializers
from tests import models as test_models


class TestUserFileUploadSerializer(dfu_serializers.AuthenticatedUploadedFileModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = dfu_serializers.UploadedFileField(required=True, allow_null=False)

    class Meta:
        model = test_models.TestUserFileUpload
        fields = ("user", "file", "created")
