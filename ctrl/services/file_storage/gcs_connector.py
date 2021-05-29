from google.cloud import storage
from config import CLOUD_STORAGE_BUCKET
import os, binascii

gcs = storage.Client(project='fii-ctrl')
bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)


def upload_file(file):
    try:
        file_extension = f".{file.filename.split('.')[1]}"
    except IndexError:
        file_extension = ''
    filename = f'{binascii.b2a_hex(os.urandom(15)).decode("utf-8")}{file_extension}'
    blob = bucket.blob(filename)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )
    return filename, blob.public_url
