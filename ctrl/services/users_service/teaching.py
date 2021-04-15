from flask_restful import Resource
from flask import make_response, jsonify
from services.auth.token_config import token_required


class Teaching(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        is_current_user_teaching = {'teaching': current_user.teaching}
        return make_response(jsonify(is_current_user_teaching), 200)
