from django.contrib import admin

from drf_file_upload import models

admin.site.register(models.AuthenticatedUploadedFile)
admin.site.register(models.AnonymousUploadedFile)
