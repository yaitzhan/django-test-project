from django.core.exceptions import ValidationError

UPLOAD_FILE_MAX_SIZE = 1024000 * 16  # 16mb


def validate_file_size(value):
    filesize = value.size

    if filesize > UPLOAD_FILE_MAX_SIZE:
        raise ValidationError("The maximum file size that can be uploaded is 16 MB")
    else:
        return value
