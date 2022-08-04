from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from tests import models, serializers


class TestUserFileUpload(viewsets.ModelViewSet):
    serializer_class = serializers.TestUserFileUploadSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.TestUserFileUpload.objects.all()

    parser_classes = [JSONParser]


class TestUserMetadataFileUpload(viewsets.ModelViewSet):
    serializer_class = serializers.TestUserFileMetadataUploadSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.TestMetadataUserFileUpload.objects.all()

    parser_classes = [JSONParser]
