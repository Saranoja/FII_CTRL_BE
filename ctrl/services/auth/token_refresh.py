from flask import make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
)
import datetime
from services.auth.token_config import refresh_token_required


class TokenRefresh(Resource):
    @staticmethod
    @refresh_token_required
    def post(current_user):
        new_token = create_access_token(identity=current_user.id, fresh=False,
                                        expires_delta=datetime.timedelta(minutes=60))
        return make_response(jsonify({'token': new_token}), 200)
