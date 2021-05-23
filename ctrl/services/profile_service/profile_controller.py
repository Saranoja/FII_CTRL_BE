import pytz
from flask_socketio import send, emit
from flask_restful import Resource
from sqlalchemy import exc
from flask import make_response, jsonify, request
from repository import TeachersSubjectsRepository, TeachersProfileDetailsRepository, UsersRepository, SubjectsRepository
from model import Announcement
from services.auth.token_config import token_required
from datetime import datetime
import logging
from config import CURRENT_TIMEZONE


# TODO: send notification to client

class ProfileController(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        teacher_id = int(request.path.split('/')[2])
        teacher_subjects = TeachersSubjectsRepository.get_subjects_for_teacher(teacher_id)
        teacher_details = TeachersProfileDetailsRepository.get_details_for_teacher(teacher_id)

        subjects = []
        for subject in teacher_subjects:
            subject_name = SubjectsRepository.get_subject_for_id(subject.subject_id).name
            subjects.append(subject_name)

        teacher = UsersRepository.get_user_for_id(teacher_id)

        details_data = {
            'name': f'{teacher.first_name} {teacher.last_name}',
            'degree': teacher_details.degree,
            'subjects': subjects,
            'email': teacher.username,
            'secondary_email': teacher_details.secondary_email,
            'phone_number': teacher_details.phone_number,
            'office': teacher_details.office_number,
            'schedule': teacher_details.schedule_url,
            'fields': teacher_details.interest_field,
            'thesis_examples': teacher_details.thesis_examples
        }

        return make_response(jsonify(details_data), 200)

    @staticmethod
    @token_required
    def patch(current_user):
        teacher_id = int(request.path.split('/')[2])

        if not current_user.teaching or current_user.id != teacher_id:
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 403)

        updated_profile_data = request.get_json()

        try:
            TeachersProfileDetailsRepository.update_details(teacher_id, updated_profile_data)
        except exc.SQLAlchemyError:
            logging.error(f"Details failed to be updated for teacher with id : {teacher_id}")
            return make_response(jsonify({"error": "Could not update details"}), 503)

        notification_data = {
            'event': 'patch',
            'type': 'success',
            'timestamp': datetime.now().timestamp(),
        }

        return make_response(jsonify({"message": "Profile updated successfully"}), 200)
