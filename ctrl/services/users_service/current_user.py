from flask_restful import Resource
from flask import make_response, jsonify
from services.auth.token_config import token_required
from repository import TeachersSubjectsRepository, SubjectsRepository


class CurrentUser(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        if current_user.teaching:
            teacher_subjects = TeachersSubjectsRepository.get_subjects_for_teacher(current_user.id)
            teacher_subjects = list(
                map(lambda x: SubjectsRepository.get_subject_for_id(x.subject_id), teacher_subjects))
            object_subjects = {}
            for subject in teacher_subjects:
                object_subjects[subject.name] = subject.id
            current_user_data = {
                'id': current_user.id, 'email': current_user.username,
                'first_name': current_user.first_name, 'last_name': current_user.last_name,
                'teaching': current_user.teaching, 'subjects': object_subjects, 'admin': current_user.admin}
        else:
            current_user_data = {
                'id': current_user.id,
                'first_name': current_user.first_name, 'last_name': current_user.last_name,
                'teaching': current_user.teaching, 'year': current_user.year,
                'group': current_user.group, 'admin': current_user.admin
            }

        return make_response(jsonify(current_user_data), 200)
