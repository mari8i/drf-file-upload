from rest_framework import mixins
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from drf_file_upload import models, serializers


class AuthenticatedFileUploadView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    parser_class = (FileUploadParser,)
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AuthenticatedUploadFileSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        return models.AuthenticatedUploadedFile.objects.filter(user_id=self.request.user.id)


class AnonymousFileUploadView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    parser_class = (FileUploadParser,)
    permission_classes = []
    serializer_class = serializers.AnonymousUploadFileSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        return models.AnonymousUploadedFile.objects.all()
