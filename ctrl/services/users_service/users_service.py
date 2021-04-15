from flask_restful import Resource
from flask import make_response, jsonify
from repository import UsersRepository
from services.auth.token_config import token_required


class UsersService(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        if not current_user.admin:
            return make_response(jsonify({'message': 'Admin rights are needed for this operation.'}), 403)
        users = UsersRepository.get_all_users()

        output = []

        for user in users:
            if not user.teaching:
                user_data = {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name,
                             'email': user.username, 'admin': user.admin, 'teaching': user.teaching, 'year': user.year,
                             'group': user.group}
            else:
                user_data = {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name,
                             'email': user.username, 'admin': user.admin, 'teaching': user.teaching}
            output.append(user_data)

        return make_response(jsonify(output), 200)
