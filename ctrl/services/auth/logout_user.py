from flask_restful import Resource
import jwt
from config import JWT_SECRET_KEY
from flask import request, make_response, jsonify
from services.auth.token_config import token_required
from datetime import datetime
from repository import TokenBlacklistRepository
from model import TokenBlacklist


class Logout(Resource):
    @staticmethod
    @token_required
    def post(current_user):
        token = request.headers.get('Authorization')
        jw_token = token.split(' ')[1]
        data = jwt.decode(jw_token, JWT_SECRET_KEY, algorithms=['HS256'])

        jti = data["jti"]
        now = datetime.now()
        blacklisted_token = TokenBlacklist(jti=jti, created_at=now)
        TokenBlacklistRepository.add_new_blacklisted_token(blacklisted_token)
        return make_response(jsonify({'message': 'Token revoked'}), 200)
