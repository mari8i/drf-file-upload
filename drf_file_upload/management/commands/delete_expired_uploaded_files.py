import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from drf_file_upload import models

logger = logging.getLogger("DrfFileUploadExpiredFiles")


class Command(BaseCommand):
    help = "Deletes expired uploaded files"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--seconds",
            type=int,
            default=600,
            required=False,
        )

    def handle(self, *args, **options):
        delete_before = timezone.now() - timedelta(seconds=options["seconds"])
        deleted, _ = models.AuthenticatedUploadedFile.objects.filter(created__lt=delete_before).delete()
        logger.info(f"Deleted {deleted} unused authenticated uploaded files")

        deleted, _ = models.AnonymousUploadedFile.objects.filter(created__lt=delete_before).delete()
        logger.info(f"Deleted {deleted} unused anonymous uploaded files")
