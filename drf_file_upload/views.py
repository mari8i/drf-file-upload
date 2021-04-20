from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from drf_file_upload import models, serializers


class AuthenticatedFileUploadView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    parser_class = [FileUploadParser, MultiPartParser]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AuthenticatedUploadFileSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        return models.AuthenticatedUploadedFile.objects.filter(user_id=self.request.user.id)

    @extend_schema(
        request=serializers.UploadFileRequestSerializer, responses={200: serializers.AuthenticatedUploadFileSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AnonymousFileUploadView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    parser_class = [FileUploadParser, MultiPartParser]
    permission_classes = []
    serializer_class = serializers.AnonymousUploadFileSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        return models.AnonymousUploadedFile.objects.all()

    @extend_schema(
        request=serializers.UploadFileRequestSerializer, responses={200: serializers.AnonymousUploadFileSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
