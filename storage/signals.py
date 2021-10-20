import json
import os

from .helpers import split_n_zip_upload_file

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import FileUpload, FileUploadSequence


@receiver(post_save, sender=FileUpload)
def create_file_upload_sequence(sender, instance, created, *args, **kwargs):
    zip_files = split_n_zip_upload_file(instance.upload.path, instance.upload.size)

    FileUploadSequence.objects.create(file_upload=instance, sequence=json.dumps(zip_files))

    try:
        os.remove(instance.upload.path)
    except FileNotFoundError as e:
        pass
