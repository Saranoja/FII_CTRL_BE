from flask_restful import Resource
from flask import request, make_response, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from flask_bcrypt import Bcrypt
from repository import UsersRepository
from config import ACCESS_EXPIRES

bcrypt = Bcrypt()


class Login(Resource):
    @staticmethod
    def post():
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response(jsonify({'message': 'Credentials are missing.'}), 401,
                                 {'WWW-Authenticate': 'Basic realm="Login required!"'})

        user = UsersRepository.get_user_by_username(username=auth.username)

        if not user:
            return make_response(jsonify({'message': 'Access denied.'}), 401,
                                 {'WWW-Authenticate': 'Basic realm="Login required!"'})

        if bcrypt.check_password_hash(user.password, auth.password):
            access_token = create_access_token(identity=user.id, fresh=True,
                                               expires_delta=ACCESS_EXPIRES)
            refresh_token = create_refresh_token(user.id)

            return make_response(jsonify({'token': access_token, 'refresh_token': refresh_token}), 200)

        return make_response(jsonify({'message': 'Access denied.'}), 401,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})
