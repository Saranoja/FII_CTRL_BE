from flask_restful import Resource
from flask import make_response, jsonify


class SanityCheck(Resource):
    @staticmethod
    def get():
        return make_response(jsonify({'message': 'Sanity check: checked :)'}), 200)
