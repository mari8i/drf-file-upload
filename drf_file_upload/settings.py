from django.conf import settings
from django.core.signals import setting_changed
from django.utils.module_loading import import_string

DEFAULTS = {
    "ALLOWED_FORMATS": None,
    "MAX_FILE_SIZE": None,
    "AUTH_MEDIA_DIR": "",
    "ANON_MEDIA_DIR": "",
    "AUTH_FILENAME_PROVIDER": "drf_file_upload.filenames.OriginalFilenameProvider",
    "ANON_FILENAME_PROVIDER": "drf_file_upload.filenames.OriginalFilenameProvider",
}

IMPORT_STRINGS = ["AUTH_FILENAME_PROVIDER", "ANON_FILENAME_PROVIDER"]


class LibSettings:
    """
    Taken from the djangorestframework library. Thanks.
    """

    def __init__(self, defaults=None, import_strings=None):
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "REST_FRAMEWORK_FILE_UPLOAD", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = import_string(val)

        # Cache the result
        self._cached_attrs.add(attr)

        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


lib_settings = LibSettings(DEFAULTS, IMPORT_STRINGS)


def reload_lib_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "REST_FRAMEWORK_FILE_UPLOAD":
        lib_settings.reload()


setting_changed.connect(reload_lib_settings)
