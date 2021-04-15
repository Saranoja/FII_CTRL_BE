from flask import make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_refresh_token,
)
from services.auth.token_config import token_required


class TokenRefresh(Resource):
    @staticmethod
    @token_required
    def post(current_user):
        new_token = create_refresh_token(current_user.id)
        return make_response(jsonify({'refresh_token': new_token}), 200)
