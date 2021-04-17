from django.urls import path, include

urlpatterns = [
    path('', include("drf_file_upload.urls")),
]
