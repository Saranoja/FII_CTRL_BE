from flask_restful import Resource
from flask import make_response, jsonify, request
from services.auth.token_config import token_required
from services.file_storage.gcs_connector import upload_file


class FilesManager(Resource):
    @staticmethod
    @token_required
    def post(current_user):
        """Process the uploaded file and upload it to Google Cloud Storage."""
        request_file = request.files.get('file')
        directory = request.args.get('dir')

        if directory is None:
            directory = ''
        else:
            directory += '/'

        if not request_file:
            return make_response(jsonify({"message": "No file uploaded."}), 400)

        stored_filename, stored_file_url = upload_file(request_file, directory)

        return make_response(jsonify({"public_url": stored_file_url, "name": stored_filename}), 200)
