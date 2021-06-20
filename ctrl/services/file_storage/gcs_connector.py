from google.cloud import storage
from config import CLOUD_STORAGE_BUCKET
from pdfminer.high_level import extract_text
import io
import logging
import xxhash
import json

gcs = storage.Client(project='fii-ctrl')
bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

BUCKET_URL = 'https://storage.googleapis.com/fii-ctrl_files'


def upload_file(file, directory):
    try:
        file_extension = f".{file.filename.split('.')[1]}"
    except IndexError:
        file_extension = ''

    does_file_exist = False
    filename = f'{directory}{file.filename}{file_extension}'

    if file.content_type == 'application/pdf':
        pdf_file = io.BytesIO(file.read())
        pdf_text = extract_text(pdf_file, maxpages=7)
        hashed_json = xxhash.xxh3_64(json.dumps(pdf_text).encode('utf-8')).hexdigest()

        does_file_exist = storage.Blob(bucket=bucket, name=f'{directory}{hashed_json}{file_extension}').exists(gcs)

        filename = f'{directory}{hashed_json}{file_extension}'
        public_url = f'{BUCKET_URL}{directory}{hashed_json}'

    if not does_file_exist:
        file.seek(0, 0)
        blob = bucket.blob(filename)
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )
        public_url = blob.public_url
    else:
        logging.info("File already exists in storage.")
    return filename, public_url
