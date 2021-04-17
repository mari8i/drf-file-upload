import io

from PIL import Image
from django.contrib.auth.models import User

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
