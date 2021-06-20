from flask_socketio import emit
from flask_restful import Resource
from sqlalchemy import exc
from flask import make_response, jsonify, request
from model import Assignment
from repository import AssignmentsRepository, DiscussionGroupsRepository, DiscussionGroupsMembersRepository, \
    UsersRepository, SubjectsRepository
from services.auth.token_config import token_required
from datetime import datetime
from io_socket import sids
import logging
from config import CURRENT_TIMEZONE


class AssignmentsController(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        user_groups = DiscussionGroupsMembersRepository.get_discussion_groups_for_user(current_user.id)
        all_assignments = []

        for group in user_groups:
            all_assignments.extend(AssignmentsRepository.get_assignments_for_group(group.discussion_group_id))

        assignments_data = []

        for assignment in all_assignments:
            author = UsersRepository.get_user_for_id(assignment.author_id)
            subject_id = assignment.subject_id
            assignments_data.append({
                "id": assignment.id,
                "title": assignment.title,
                "subject_id": subject_id,
                "subject": SubjectsRepository.get_subject_for_id(subject_id).name,
                "description": assignment.description,
                "author": f'{author.first_name} {author.last_name}',
                "author_id": assignment.author_id,
                "created_at": assignment.created_at,
                "deadline": assignment.deadline,
                "discussion_group_id": assignment.discussion_group_id,
                "file_url": assignment.file_url
            })

        return make_response(jsonify(assignments_data), 200)

    @staticmethod
    @token_required
    def post(current_user):
        if not current_user.teaching:
            return make_response(jsonify({'message': 'User must be a teacher for this operation.'}), 403)

        group_id = request.path.split('/')[2]
        if not DiscussionGroupsMembersRepository.is_member_in_group(current_user.id, group_id):
            return make_response(jsonify({"error": "Missing authorization to post in this group."}), 403)

        assignment_data = request.get_json()

        try:
            new_assignment = Assignment(title=assignment_data["title"], description=assignment_data["description"],
                                        author_id=current_user.id,
                                        created_at=datetime.now(CURRENT_TIMEZONE),
                                        discussion_group_id=group_id,
                                        deadline=assignment_data["deadline"],
                                        subject_id=assignment_data["subject_id"],
                                        file_url=assignment_data["file_url"])
            AssignmentsRepository.add_new_assignment(new_assignment)
            logging.info(
                f"New assignment posted in : {group_id} by {current_user.username} for {assignment_data['subject_id']}")
        except exc.SQLAlchemyError:
            logging.error(f"Assignment failed to be posted in : {group_id} by {current_user.id}")
            notification_data = {
                'domain': 'assignments',
                'event': 'post',
                'type': 'error',
                'author_id': current_user.id,
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
                'group_id': group_id,
                'timestamp': datetime.now().timestamp(),
            }
            emit('error_assignment', notification_data, broadcast=True, namespace='', to=sids[current_user.id])
            return make_response(jsonify({"error": "Could not add new assignment"}), 503)
        except KeyError:
            return make_response(jsonify({"error": "Assignment structure incomplete"}), 400)

        notification_data = {
            'domain': 'assignments',
            'event': 'post',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
            'group_id': group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        emit('assignment', notification_data, broadcast=True, namespace='', to=group_id)
        return make_response(jsonify({"message": "New assignment posted successfully"}), 202)

    @staticmethod
    @token_required
    def delete(current_user):
        group_id = request.path.split('/')[2]
        assignment_id = request.args.get('id')
        assignment_author_id = AssignmentsRepository.get_assignment_with_id(assignment_id).author_id

        if not current_user.teaching \
                or current_user.id != assignment_author_id:
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 401)

        try:
            AssignmentsRepository.delete_assignment(assignment_id)
        except exc.SQLAlchemyError:
            notification_data = {
                'domain': 'assignments',
                'event': 'delete',
                'type': 'error',
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
                'group_id': group_id,
                'author': f'{current_user.first_name} {current_user.last_name}',
                'author_id': current_user.id,
                'timestamp': datetime.now().timestamp(),
            }
            emit('error_assignment', notification_data, broadcast=True, namespace='', to=sids[current_user.id])
            logging.error(f"Failed to delete assignment with id : {assignment_id}")
            return make_response(jsonify({"error": f"Failed to delete assignment for id {assignment_id}."}), 503)

        notification_data = {
            'domain': 'assignments',
            'event': 'delete',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
            'group_id': group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        emit('assignment', notification_data, broadcast=True, namespace='', to=group_id)
        return make_response(jsonify({"message": "Assignment deleted successfully"}), 200)

    @staticmethod
    @token_required
    def patch(current_user):
        group_id = request.path.split('/')[2]

        assignment_id = request.args.get('id')
        assignment_author_id = AssignmentsRepository.get_assignment_with_id(assignment_id).author_id

        if not current_user.teaching \
                or not DiscussionGroupsMembersRepository.is_member_in_group(current_user.id, group_id) \
                or current_user.id != assignment_author_id:
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 401)

        updated_assignment_data = request.get_json()

        try:
            AssignmentsRepository.update_assignment(assignment_id, updated_assignment_data)
        except exc.SQLAlchemyError:
            notification_data = {
                'domain': 'assignments',
                'event': 'patch',
                'type': 'error',
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
                'group_id': group_id,
                'author': f'{current_user.first_name} {current_user.last_name}',
                'author_id': current_user.id,
                'timestamp': datetime.now().timestamp(),
            }
            emit('error_assignment', notification_data, broadcast=True, namespace='', to=sids[current_user.id])
            logging.error(f"Assignment failed to be updated in : {group_id}")
            return make_response(jsonify({"error": "Could not update assignment"}), 503)

        notification_data = {
            'domain': 'assignments',
            'event': 'patch',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
            'group_id': group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        emit('assignment', notification_data, broadcast=True, namespace='', to=group_id)
        return make_response(jsonify({"message": "Assignment updated successfully"}), 200)
