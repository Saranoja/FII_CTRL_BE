from flask_restful import Resource
from flask import make_response, jsonify, request
from repository import UsersRepository
from services.auth.token_config import token_required


class StudentsService(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        students_year = request.args.get('year')
        students_group = request.args.get('group')

        if students_year and students_group:
            students = UsersRepository.get_students_from_year_group(students_year, students_group)
        else:
            students = UsersRepository.get_all_students()

        output = []

        for student in students:
            user_data = {'id': student.id, 'first_name': student.first_name, 'last_name': student.last_name,
                         'email': student.username, 'group': student.group, 'year': student.year}
            output.append(user_data)

        return make_response(jsonify(output), 200)
