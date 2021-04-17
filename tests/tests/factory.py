import io
from datetime import datetime

import pytz
from PIL import Image
from django.contrib.auth.models import User
from django.core.files import File

from drf_file_upload import models

USERNAME = "test_upload"
PASSWORD = "test_upload!"


def create_simple_uploaded_file(filename="best_file_eva.pdf", size=(100, 100), color=(155, 0, 0)):
    file = io.BytesIO()
    image = Image.new("RGBA", size=size, color=color)
    image.save(file, "png")
    file.name = filename
    file.seek(0)
    return file


def create_user():
    return User.objects.create_user(username=USERNAME, password=PASSWORD)


def create_datetime(year, month, day, hour, minutes=0, seconds=0):
    mock_date = datetime(year, month, day, hour, minutes, seconds)
    tz = pytz.timezone("Europe/Rome")
    mock_date = tz.localize(mock_date)
    return mock_date


def create_authenticated_uploaded_file(user, filename="test_file.pdf", size=(100, 100)):
    file_contents = create_simple_uploaded_file(filename=filename, size=size)
    return models.AuthenticatedUploadedFile.objects.create(file=File(file_contents), user=user)


def create_anonymous_uploaded_file(filename="test_file.pdf", size=(100, 100)):
    file_contents = create_simple_uploaded_file(filename=filename, size=size)
    return models.AnonymousUploadedFile.objects.create(file=File(file_contents))
