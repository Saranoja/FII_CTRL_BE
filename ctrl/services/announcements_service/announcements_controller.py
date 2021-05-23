import pytz
from flask_socketio import send, emit
from flask_restful import Resource
from sqlalchemy import exc
from flask import make_response, jsonify, request
from repository import AnnouncementsRepository, DiscussionGroupsRepository, DiscussionGroupsMembersRepository, \
    UsersRepository
from model import Announcement
from services.auth.token_config import token_required
from datetime import datetime
import logging
from config import CURRENT_TIMEZONE


# TODO: check for pagination on GET method

class AnnouncementsController(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        req_group_id = int(request.path.split('/')[2])
        announcements = AnnouncementsRepository.get_announcements_for_group(req_group_id)

        announcements_extended = []

        for announcement in announcements:
            author = UsersRepository.get_user_for_id(announcement.author_id)
            announcements_extended.append({
                "id": announcement.id,
                "title": announcement.title,
                "text": announcement.text,
                "author": f'{author.first_name} {author.last_name}',
                "author_id": announcement.author_id,
                "created_at": announcement.created_at.replace(tzinfo=pytz.utc).astimezone(CURRENT_TIMEZONE),
                "discussion_group_id": announcement.discussion_group_id
            })

        return make_response(jsonify(announcements_extended), 200)

    @staticmethod
    @token_required
    def post(current_user):
        if not current_user.teaching:
            return make_response(jsonify({'message': 'User must be a teacher for this operation.'}), 403)

        group_id = request.path.split('/')[2]
        if not DiscussionGroupsMembersRepository.is_member_in_group(current_user.id, group_id):
            return make_response(jsonify({"error": "Missing authorization to post in this group."}), 403)

        announcement_data = request.get_json()

        try:
            new_announcement = Announcement(title=announcement_data["title"], text=announcement_data["text"],
                                            author_id=current_user.id,
                                            created_at=datetime.now(CURRENT_TIMEZONE),
                                            discussion_group_id=group_id)
            AnnouncementsRepository.add_new_announcement(new_announcement)
            logging.info(f"New announcement posted in : {group_id} by {current_user.username}")
        except exc.SQLAlchemyError:
            logging.error(f"Announcement failed to be posted in : {group_id} by {current_user.id}")
            notification_data = {
                'event': 'post',
                'type': 'error',
                'author_id': current_user.id,
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
                'group_id': group_id,
                'timestamp': datetime.now().timestamp(),
            }
            emit('error', notification_data, broadcast=True, namespace='', to=int(group_id))
            return make_response(jsonify({"error": "Could not add new announcement"}), 503)
        except KeyError:
            return make_response(jsonify({"error": "Announcement structure incomplete"}), 400)

        notification_data = {
            'event': 'post',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
            'group_id': group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        send(notification_data, broadcast=True, namespace='', to=int(group_id))
        return make_response(jsonify({"message": "New announcement posted successfully"}), 202)

    @staticmethod
    @token_required
    def patch(current_user):
        group_id = request.path.split('/')[2]

        announcement_id = request.args.get('id')
        announcement_author_id = AnnouncementsRepository.get_announcement_with_id(announcement_id).author_id

        if not current_user.teaching \
                or not DiscussionGroupsMembersRepository.is_member_in_group(current_user.id, group_id) \
                or current_user.id != announcement_author_id:
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 401)

        updated_announcement_data = request.get_json()
        print(updated_announcement_data)

        try:
            AnnouncementsRepository.update_announcement(announcement_id, updated_announcement_data)
        except exc.SQLAlchemyError:
            notification_data = {
                'event': 'patch',
                'type': 'error',
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
                'group_id': group_id,
                'author': f'{current_user.first_name} {current_user.last_name}',
                'author_id': current_user.id,
                'timestamp': datetime.now().timestamp(),
            }
            send(notification_data, broadcast=True, namespace='', to=int(group_id))
            logging.error(f"Announcement failed to be updated in : {group_id}")
            return make_response(jsonify({"error": "Could not update announcement"}), 503)

        notification_data = {
            'event': 'patch',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
            'group_id': group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        send(notification_data, broadcast=True, namespace='', to=int(group_id))
        return make_response(jsonify({"message": "Announcement updated successfully"}), 200)

    @staticmethod
    @token_required
    def delete(current_user):
        group_id = request.path.split('/')[2]
        announcement_id = request.args.get('id')
        announcement_author_id = AnnouncementsRepository.get_announcement_with_id(announcement_id).author_id

        if not current_user.teaching \
                or not DiscussionGroupsMembersRepository.is_member_in_group(current_user.id, group_id) \
                or current_user.id != announcement_author_id:
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 401)

        try:
            AnnouncementsRepository.delete_announcement(announcement_id)
        except exc.SQLAlchemyError:
            notification_data = {
                'event': 'delete',
                'type': 'error',
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
                'group_id': group_id,
                'author': f'{current_user.first_name} {current_user.last_name}',
                'author_id': current_user.id,
                'timestamp': datetime.now().timestamp(),
            }
            emit('error', notification_data, broadcast=True, namespace='', to=int(group_id))
            logging.error(f"Failed to delete announcement with id : {announcement_id}")
            return make_response(jsonify({"error": f"Failed to delete announcement for id {announcement_id}."}), 503)

        notification_data = {
            'event': 'delete',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
            'group_id': group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        send(notification_data, broadcast=True, namespace='', to=int(group_id))
        return make_response(jsonify({"message": "Announcement deleted successfully"}), 200)
