import logging
from datetime import timedelta

from django.utils import timezone

from drf_file_upload import models

logger = logging.getLogger("DrfFileUploadExpiredFiles")


def cleanup_expired_uploaded_files(expiration_seconds):
    delete_before = timezone.now() - timedelta(seconds=expiration_seconds)
    deleted, _ = models.AuthenticatedUploadedFile.objects.filter(created__lt=delete_before).delete()
    logger.info(f"Deleted {deleted} unused authenticated uploaded files")

    deleted, _ = models.AnonymousUploadedFile.objects.filter(created__lt=delete_before).delete()
    logger.info(f"Deleted {deleted} unused anonymous uploaded files")
