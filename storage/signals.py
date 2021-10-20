import json
import os
import logging

from .helpers import split_n_zip_upload_file

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import FileUpload, FileUploadSequence


logger = logging.getLogger('app-logger')


@receiver(post_save, sender=FileUpload)
def create_file_upload_sequence(sender, instance, created, *args, **kwargs):
    zip_files = split_n_zip_upload_file(instance.upload.path, instance.upload.size)

    FileUploadSequence.objects.create(file_upload=instance, sequence=json.dumps(zip_files))

    logger.info(f'Created new FileUploadSequence object for FileUpload object: {instance.id}')
    try:
        os.remove(instance.upload.path)
    except FileNotFoundError:
        pass
