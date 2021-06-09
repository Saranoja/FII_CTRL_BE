from flask_restful import Resource
from sqlalchemy import exc
from flask import make_response, jsonify, request
from repository import DiscussionGroupsMembersRepository, UsersRepository
from services.auth.token_config import token_required


class GroupsMembersController(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        group_id = request.path.split('/')[2]

        is_user_member = DiscussionGroupsMembersRepository.is_member_in_group(current_user.id, group_id)
        if not current_user.admin and not (is_user_member and current_user.teaching):
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 401)

        members_list = []

        try:
            group_members_ids = list(
                map(lambda x: x.user_id, DiscussionGroupsMembersRepository.get_members_for_group(group_id)))
            for mid in group_members_ids:
                member = UsersRepository.get_user_for_id(mid)
                members_list.append(
                    {
                        'id': member.id,
                        'first_name': member.first_name,
                        'last_name': member.last_name,
                        'group': member.group,
                        'year': member.year,
                        'teaching': member.teaching,
                    }
                )
        except exc.SQLAlchemyError:
            return make_response(jsonify({'message': 'Error while retrieving users from group.'}), 503)

        return make_response(jsonify({'members': members_list}), 200)

    @staticmethod
    @token_required
    def put(current_user):
        group_id = request.path.split('/')[2]
        new_users_ids = request.get_json()['id']

        is_user_member = DiscussionGroupsMembersRepository.is_member_in_group(current_user.id, group_id)
        if not current_user.admin and not (is_user_member and current_user.teaching):
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 401)

        try:
            for uid in new_users_ids:
                DiscussionGroupsMembersRepository.add_new_member_to_group(uid, group_id)
        except exc.SQLAlchemyError:
            return make_response(jsonify({'message': 'Error while adding users to group.'}), 503)

        return make_response(jsonify({'message': 'Users added successfully.'}), 200)

    @staticmethod
    @token_required
    def delete(current_user):
        group_id = request.path.split('/')[2]
        deleting_users_ids = request.get_json()['id']

        is_user_member = DiscussionGroupsMembersRepository.is_member_in_group(current_user.id, group_id)
        if not current_user.admin and not (is_user_member and current_user.teaching):
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 401)

        try:
            for uid in deleting_users_ids:
                DiscussionGroupsMembersRepository.delete_member_from_group(uid, group_id)
        except exc.SQLAlchemyError:
            return make_response(jsonify({'message': 'Error while deleting user from group.'}), 503)

        return make_response(jsonify({'message': 'Users removed successfully.'}), 200)
