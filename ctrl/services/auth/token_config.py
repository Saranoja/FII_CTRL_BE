from flask import request, make_response, jsonify
import jwt
import functools
from repository import UsersRepository
from config import JWT_SECRET_KEY


def token_required(f, fresh=False):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return make_response(jsonify({'message': 'Token is missing.'}), 401)

        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            if fresh and not data['fresh']:
                return make_response(jsonify({'message': 'Token not fresh.'}), 401)
            current_user = UsersRepository.is_user_valid(id=data['sub'])
        except Exception as e:
            return make_response(jsonify({'message': 'Token is invalid.'}), 401)

        return f(current_user)

    return decorated
