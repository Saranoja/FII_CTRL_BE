from flask_socketio import emit
from flask_restful import Resource
from sqlalchemy import exc
from flask import make_response, jsonify, request
from repository import MeetingsRepository, DiscussionGroupsRepository, DiscussionGroupsMembersRepository, \
    UsersRepository
from model import Meeting
from services.auth.token_config import token_required
from datetime import datetime, timedelta
import logging
from io_socket import sids
from config import CURRENT_TIMEZONE


class MeetingsController(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        user_groups = DiscussionGroupsMembersRepository.get_discussion_groups_for_user(current_user.id)

        meetings = []

        for group in user_groups:
            meetings.extend(MeetingsRepository.get_meetings_for_group(group.discussion_group_id))
        meetings_extended = []

        for meeting in meetings:
            author = UsersRepository.get_user_for_id(meeting.author_id)
            next_meeting_occurrence = meeting.timestamp
            if meeting.recurrent:
                while next_meeting_occurrence < datetime.now(CURRENT_TIMEZONE) - timedelta(minutes=30):
                    next_meeting_occurrence += meeting.recurrence_interval

            if next_meeting_occurrence > datetime.now(CURRENT_TIMEZONE) - timedelta(minutes=30):
                is_joining_permitted = False

                if abs(next_meeting_occurrence - datetime.now(CURRENT_TIMEZONE)) < timedelta(minutes=30):
                    is_joining_permitted = True

                recurrence_interval = meeting.recurrence_interval
                if recurrence_interval is not None:
                    recurrence_interval = str(meeting.recurrence_interval).split(',')[0]

                meetings_extended.append({
                    "id": meeting.id,
                    "title": meeting.title,
                    "url": meeting.url,
                    "author": f'{author.first_name} {author.last_name}',
                    "author_id": meeting.author_id,
                    "timestamp": meeting.timestamp,
                    "group_id": meeting.group_id,
                    "recurrent": meeting.recurrent,
                    "recurrence_interval": recurrence_interval,
                    "next_occurrence": next_meeting_occurrence,
                    "is_joining_permitted": is_joining_permitted
                })
        return make_response(jsonify(meetings_extended), 200)

    @staticmethod
    @token_required
    def post(current_user):
        if not current_user.teaching:
            return make_response(jsonify({'message': 'User must be a teacher for this operation.'}), 403)

        meeting_data = request.get_json()

        try:
            if not DiscussionGroupsMembersRepository.is_member_in_group(current_user.id, meeting_data["group_id"]):
                return make_response(jsonify({"error": "Missing authorization to post in this group."}), 403)
        except KeyError:
            return make_response(jsonify({"error": "Meeting structure incomplete"}), 400)

        try:
            new_meeting = Meeting(title=meeting_data["title"], url=meeting_data["url"],
                                  author_id=current_user.id,
                                  timestamp=meeting_data["timestamp"],
                                  recurrent=meeting_data["recurrent"],
                                  recurrence_interval=meeting_data["recurrence_interval"],
                                  group_id=meeting_data["group_id"])
            MeetingsRepository.add_new_meeting(new_meeting)
            logging.info(f"New meeting posted in : {meeting_data['group_id']} by {current_user.username}")
        except exc.SQLAlchemyError:
            logging.error(f"Meeting failed to be posted in : {meeting_data['group_id']} by {current_user.id}")
            notification_data = {
                'domain': 'meetings',
                'event': 'post',
                'type': 'error',
                'author_id': current_user.id,
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(meeting_data['group_id']).name,
                'group_id': meeting_data['group_id'],
                'timestamp': datetime.now().timestamp(),
            }
            emit('error_meetings', notification_data, broadcast=True, namespace='', to=sids[current_user.id])
            return make_response(jsonify({"error": "Could not add new meeting"}), 503)
        except KeyError:
            return make_response(jsonify({"error": "Meeting structure incomplete"}), 400)

        notification_data = {
            'domain': 'meetings',
            'event': 'post',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(meeting_data['group_id']).name,
            'group_id': meeting_data['group_id'],
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        emit('meetings', notification_data, broadcast=True, namespace='', to=str(meeting_data['group_id']))
        return make_response(jsonify({"message": "New meeting posted successfully"}), 202)

    @staticmethod
    @token_required
    def patch(current_user):
        meeting_id = request.args.get('id')

        meeting = MeetingsRepository.get_meeting_for_id(meeting_id)
        meeting_author_id = meeting.author_id
        group_id = str(meeting.group_id)

        if not current_user.teaching \
                or not DiscussionGroupsMembersRepository.is_member_in_group(current_user.id,
                                                                            group_id) \
                or current_user.id != meeting_author_id:
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 401)

        updated_meeting_data = request.get_json()

        try:
            MeetingsRepository.update_meeting(meeting_id, updated_meeting_data)
        except exc.SQLAlchemyError:
            notification_data = {
                'domain': 'meetings',
                'event': 'patch',
                'type': 'error',
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
                'group_id': group_id,
                'author': f'{current_user.first_name} {current_user.last_name}',
                'author_id': current_user.id,
                'timestamp': datetime.now().timestamp(),
            }
            emit('error_meetings', notification_data, broadcast=True, namespace='', to=sids[current_user.id])
            logging.error(f"Meeting failed to be updated in : {group_id}")
            return make_response(jsonify({"error": "Could not update meeting"}), 503)

        notification_data = {
            'domain': 'meetings',
            'event': 'patch',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
            'group_id': group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        emit('meetings', notification_data, broadcast=True, namespace='', to=group_id)
        return make_response(jsonify({"message": "Meeting updated successfully"}), 200)

    @staticmethod
    @token_required
    def delete(current_user):
        meeting_id = request.args.get('id')

        meeting = MeetingsRepository.get_meeting_for_id(meeting_id)
        meeting_author_id = meeting.author_id
        group_id = str(meeting.group_id)

        if not current_user.teaching \
                or not DiscussionGroupsMembersRepository.is_member_in_group(current_user.id, group_id) \
                or current_user.id != meeting_author_id:
            return make_response(jsonify({'message': 'Unauthorized for this operation.'}), 401)

        try:
            MeetingsRepository.delete_meeting(meeting_id)
        except exc.SQLAlchemyError:
            notification_data = {
                'domain': 'meetings',
                'event': 'delete',
                'type': 'error',
                'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
                'group_id': group_id,
                'author': f'{current_user.first_name} {current_user.last_name}',
                'author_id': current_user.id,
                'timestamp': datetime.now().timestamp(),
            }
            emit('error_meetings', notification_data, broadcast=True, namespace='', to=sids[current_user.id])
            logging.error(f"Failed to delete meeting with id : {meeting_id}")
            return make_response(jsonify({"error": f"Failed to delete meeting for id {meeting_id}."}), 503)

        notification_data = {
            'domain': 'meetings',
            'event': 'delete',
            'type': 'success',
            'group': DiscussionGroupsRepository.get_discussion_group_for_id(group_id).name,
            'group_id': group_id,
            'author': f'{current_user.first_name} {current_user.last_name}',
            'author_id': current_user.id,
            'timestamp': datetime.now().timestamp(),
        }
        emit('meetings', notification_data, broadcast=True, namespace='', to=group_id)
        return make_response(jsonify({"message": "Meeting deleted successfully"}), 200)
