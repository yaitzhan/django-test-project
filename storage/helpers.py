import os
import zipfile
import uuid
import json

from django.conf import settings

FILE_COUNT = 16


# TODO change with custom FileUploadHandler + source file deletion after upload
def split_n_zip_upload_file(file_path: str, file_size: int) -> list:
    chunk_size = file_size // 16

    chunks = [chunk_size for i in range(15)]
    chunks.append(chunk_size + file_size % 16)

    result = []
    with open(file_path, 'rb') as f:
        for idx, size in enumerate(chunks):
            chunk = f.read(size)
            buff_file_name = str(uuid.uuid4())
            zip_file_name = f'{buff_file_name}.zip'

            with zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, zip_file_name),
                                 'w',
                                 zipfile.ZIP_DEFLATED) as zipf:
                zipf.writestr(buff_file_name, chunk)

            result.append(zip_file_name)

    return result


def combine_result_file_from_zips(zip_list_str: str, file_name):
    zip_list = json.loads(zip_list_str)
    with open(os.path.join(settings.MEDIA_ROOT, file_name), 'wb') as fff:
        for file in zip_list:
            with zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, file), 'r') as zipf:
                with zipf.open(file.split('.')[0]) as ff:
                    fff.write(ff.read())
