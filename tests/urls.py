from django.urls import include, path

urlpatterns = [
    path("", include("drf_file_upload.urls")),
]
