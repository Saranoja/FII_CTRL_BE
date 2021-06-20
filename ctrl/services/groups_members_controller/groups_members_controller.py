from flask_restful import Resource
from sqlalchemy import exc
from flask import make_response, jsonify, request
from repository import DiscussionGroupsMembersRepository, UsersRepository, DiscussionGroupsRepository
from flask_socketio import emit
from datetime import datetime
from io_socket import sids
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
            notification_data = {
                'domain': 'members',
                'event': 'put',
                'type': 'error',
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
                'group_id': group_id,
                'author': f'{current_user.first_name} {current_user.last_name}',
                'author_id': current_user.id,
                'timestamp': datetime.now().timestamp(),
            }
            emit('error_members', notification_data, broadcast=True, namespace='', to=sids[current_user.id])
            return make_response(jsonify({'message': 'Error while adding users to group.'}), 503)

        notification_data = {
            'domain': 'members',
            'event': 'put',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
            'group_id': group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        new_user_sids = []
        try:
            for new_user_id in new_users_ids:
                new_user_sids.append(sids[new_user_id])
            new_user_sids.append(sids[current_user.id])
        except KeyError:
            pass  # request author went offline in the meantime

        print(new_user_sids)
        print(sids)
        print(current_user)
        emit('members', notification_data, broadcast=True, namespace='', to=new_user_sids)
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
            notification_data = {
                'domain': 'members',
                'event': 'delete',
                'type': 'error',
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
                'group_id': group_id,
                'author': f'{current_user.first_name} {current_user.last_name}',
                'author_id': current_user.id,
                'timestamp': datetime.now().timestamp(),
            }
            emit('error_members', notification_data, broadcast=True, namespace='', to=sids[current_user.id])
            return make_response(jsonify({'message': 'Error while deleting user from group.'}), 503)

        notification_data = {
            'domain': 'members',
            'event': 'delete',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
            'group_id': group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        deleting_user_sids = []
        try:
            for new_user_id in deleting_users_ids:
                deleting_user_sids.append(sids[new_user_id])
            deleting_user_sids.append(sids[current_user.id])
        except KeyError:
            pass  # request author went offline in the meantime
        emit('members', notification_data, broadcast=True, namespace='',
             to=deleting_user_sids)
        return make_response(jsonify({'message': 'Users removed successfully.'}), 200)
