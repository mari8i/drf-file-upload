import logging

from django.core.management.base import BaseCommand

from drf_file_upload.cleanup import cleanup_expired_uploaded_files

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
        logger.info("Cleaning up expired uploaded files")
        cleanup_expired_uploaded_files(options["seconds"])
