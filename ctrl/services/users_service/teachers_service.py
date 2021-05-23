from flask_restful import Resource
from flask import make_response, jsonify
from repository import UsersRepository
from services.auth.token_config import token_required


class TeachersService(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        teachers = UsersRepository.get_all_teachers()

        output = []

        for teacher in teachers:
            user_data = {'id': teacher.id, 'first_name': teacher.first_name, 'last_name': teacher.last_name,
                         'email': teacher.username}
            output.append(user_data)

        return make_response(jsonify(output), 200)
