from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tests import views

router = DefaultRouter()
router.register(r"test-upload-auth", views.TestUserFileUpload, basename="test_upload_auth")
router.register(r"test-upload-auth-meta", views.TestUserMetadataFileUpload, basename="test_upload_auth_meta")

urlpatterns = [
    path("", include("drf_file_upload.urls")),
] + router.urls
