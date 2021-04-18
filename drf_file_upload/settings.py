from django.conf import settings

ALLOWED_FORMATS = "allowed_formats"
MAX_FILE_SIZE = "max_file_size"


def get_setting_or_default(name, default):
    if hasattr(settings, "REST_FRAMEWORK_FILE_UPLOAD") and name in settings.REST_FRAMEWORK_FILE_UPLOAD:
        return settings.REST_FRAMEWORK_FILE_UPLOAD[name]
    return default
