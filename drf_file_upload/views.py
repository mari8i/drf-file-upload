from rest_framework import mixins
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from drf_file_upload import serializers, models


class AuthenticatedFileUploadView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    parser_class = (FileUploadParser,)
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AuthenticatedUploadFileSerializer

    def get_queryset(self):
        return models.AuthenticatedUploadedFile.objects.filter(user_id=self.request.user.id)


class AnonymousFileUploadView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    parser_class = (FileUploadParser,)
    permission_classes = []
    serializer_class = serializers.AnonymousUploadFileSerializer

    def get_queryset(self):
        return models.AnonymousUploadedFile.objects.all()
