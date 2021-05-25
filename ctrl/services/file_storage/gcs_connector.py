from google.cloud import storage
from config import CLOUD_STORAGE_BUCKET
import os, binascii

gcs = storage.Client(project='fii-ctrl')
bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)


def upload_file(file):
    filename = binascii.b2a_hex(os.urandom(15))
    blob = bucket.blob(filename)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )
    return filename, blob.public_url
