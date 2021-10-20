from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_file_size


class FileUpload(models.Model):
    name = models.CharField(max_length=100)
    upload = models.FileField(validators=[validate_file_size])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Файл")
        verbose_name_plural = _("Файлы")

    def __str__(self):
        return self.name


class FileUploadSequence(models.Model):
    file_upload = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name="zip_files")
    sequence = models.TextField()

    class Meta:
        verbose_name = _("Zip Файл")
        verbose_name_plural = _("Zip Файлы")

    def __str__(self):
        return self.file_upload.name
