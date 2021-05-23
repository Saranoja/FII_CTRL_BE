from flask_restful import Resource
from sqlalchemy import exc
from flask import make_response, jsonify, request
from repository import DiscussionGroupsMembersRepository, DiscussionGroupsRepository
from services.auth.token_config import token_required


class GroupsMembersController(Resource):
    @staticmethod
    @token_required
    def put(current_user):
        if not current_user.teaching:
            return make_response(jsonify({'message': 'User must be a teacher for this operation.'}), 403)

        group_id = request.path.split('/')[2]
        new_users_ids = request.get_json()['id']

        is_user_member = DiscussionGroupsMembersRepository.is_member_in_group(current_user.id, group_id)
        if not is_user_member:
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 403)

        try:
            for uid in new_users_ids:
                DiscussionGroupsMembersRepository.add_new_member_to_group(uid, group_id)
        except exc.SQLAlchemyError:
            return make_response(jsonify({'message': 'Error while adding users to group.'}), 200)

        return make_response(jsonify({'message': 'Users added successfully.'}), 200)
