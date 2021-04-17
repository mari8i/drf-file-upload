from django.urls import include, path
from rest_framework import routers

from drf_file_upload import views

router = routers.SimpleRouter()
router.register(r"upload", views.AuthenticatedFileUploadView, basename="authenticated-upload")
router.register(
    r"anonymous-upload",
    views.AnonymousFileUploadView,
    basename="anonymous-upload",
)

urlpatterns = [
    path("", include(router.urls)),
]
