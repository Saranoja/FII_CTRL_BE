from flask_restful import Resource
from sqlalchemy import exc
from flask_socketio import emit
from datetime import datetime
from io_socket import sids
from flask import make_response, jsonify, request
from repository import DiscussionGroupsMembersRepository, DiscussionGroupsRepository
from model import DiscussionGroup
from services.auth.token_config import token_required
import logging


class GroupsController(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        current_user_groups = DiscussionGroupsMembersRepository.get_discussion_groups_for_user(current_user.id)
        current_user_groups_extended = []
        for group in current_user_groups:
            valid_discussion_group = DiscussionGroupsRepository.get_discussion_group_for_id(group.discussion_group_id)
            current_user_groups_extended.append({
                "name": valid_discussion_group.name,
                "id": valid_discussion_group.id,
                "avatar": valid_discussion_group.avatar,
            })

        return make_response(jsonify({'current_user_groups': current_user_groups_extended}), 200)

    @staticmethod
    @token_required
    def post(current_user):
        if not current_user.admin and not current_user.teaching:
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 403)

        request_body = request.get_json()
        try:
            added_members_ids = request_body['members']
            new_group_name = request_body['name']
        except KeyError:
            return make_response(jsonify({'message': 'Body missing name or members field.'}), 400)

        new_group = DiscussionGroup(name=new_group_name)
        added_members_ids.append(current_user.id)
        new_group_id = -1

        try:
            new_group_id = DiscussionGroupsRepository.add_new_discussion_group(new_group)
            for uid in added_members_ids:
                DiscussionGroupsMembersRepository.add_new_member_to_group(uid, new_group_id)
        except exc.SQLAlchemyError:
            notification_data = {
                'domain': 'groups',
                'event': 'post',
                'type': 'error',
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(new_group_id).name,
                'group_id': new_group_id,
                'author': f'{current_user.first_name} {current_user.last_name}',
                'author_id': current_user.id,
                'timestamp': datetime.now().timestamp(),
            }
            emit('error_groups', notification_data, broadcast=True, namespace='', to=sids[current_user.id])
            return make_response(jsonify({'message': 'Error while creating new group.'}), 503)

        notification_data = {
            'domain': 'groups',
            'event': 'post',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(new_group_id).name,
            'group_id': new_group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        all_current_sockets = list(map(lambda y: sids[y], filter(lambda x: x in added_members_ids, sids)))
        for user_socket in all_current_sockets:
            emit('groups', notification_data, broadcast=True, namespace='', to=user_socket)

        return make_response(jsonify({'message': 'Group created successfully.'}), 200)

    @staticmethod
    @token_required
    def delete(current_user):
        group_id = request.args.get('id')
        if group_id is None:
            return make_response(jsonify({'message': 'Missing id field.'}), 400)

        if not current_user.admin and not current_user.teaching and not DiscussionGroupsMembersRepository.is_member_in_group(
                current_user.id,
                group_id):
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 401)

        group_name = DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name

        try:
            DiscussionGroupsRepository.delete_group(group_id)
            DiscussionGroupsMembersRepository.delete_all_members_from_group(group_id)
        except exc.SQLAlchemyError:
            notification_data = {
                'domain': 'groups',
                'event': 'delete',
                'type': 'error',
                'group': group_name,
                'group_id': group_id,
                'author': f'{current_user.first_name} {current_user.last_name}',
                'author_id': current_user.id,
                'timestamp': datetime.now().timestamp(),
            }
            emit('error_groups', notification_data, broadcast=True, namespace='', to=sids[current_user.id])
            return make_response(jsonify({'message': 'Error while deleting group.'}), 503)

        notification_data = {
            'domain': 'groups',
            'event': 'delete',
            'type': 'success',
            'group': group_name,
            'group_id': group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        emit('groups', notification_data, broadcast=True, namespace='', to=int(group_id))
        return make_response(jsonify({'message': 'Group deleted successfully.'}), 200)

    @staticmethod
    @token_required
    def patch(current_user):
        group_id = request.args.get('id')

        if group_id is None:
            return make_response(jsonify({'message': 'Missing id field.'}), 400)

        if not current_user.admin and not current_user.teaching and not DiscussionGroupsMembersRepository.is_member_in_group(
                current_user.id,
                group_id):
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 401)

        updated_group_data = request.get_json()

        try:
            DiscussionGroupsRepository.update_group(group_id, updated_group_data)
        except exc.SQLAlchemyError:
            return make_response(jsonify({'message': 'Error while updating group.'}), 503)

        return make_response(jsonify({'message': 'Group updated successfully.'}), 200)
