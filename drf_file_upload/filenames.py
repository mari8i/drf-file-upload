import uuid
from abc import ABC, abstractmethod

# TODO: Test these


class BaseFilenameProvider(ABC):
    @abstractmethod
    def get_filename(self, original_filename, user=None):
        pass


class OriginalFilenameProvider(BaseFilenameProvider):
    def get_filename(self, original_filename, user=None):
        return original_filename


class UUIDFilenameProvider(BaseFilenameProvider):
    def get_filename(self, original_filename, user=None):
        ext = original_filename.split(".")[-1]
        return "%s.%s" % (uuid.uuid4(), ext)
