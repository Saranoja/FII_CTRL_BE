import pytz
from flask_restful import Resource
from sqlalchemy import exc
from flask import make_response, jsonify, request
from repository import AnnouncementsRepository
from model import Announcement
from services.auth.token_config import token_required
from datetime import datetime
import logging
from config import CURRENT_TIMEZONE


class AnnouncementsController(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        req_group_id = int(request.path.split('/')[2])
        announcements = AnnouncementsRepository.get_announcements_for_group(req_group_id)

        announcements_extended = []

        for announcement in announcements:
            announcements_extended.append({
                "title": announcement.title,
                "text": announcement.text,
                "author": announcement.author,
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
        announcement_data = request.get_json()

        try:
            new_announcement = Announcement(title=announcement_data["title"], text=announcement_data["text"],
                                            author=announcement_data["author"],
                                            created_at=datetime.now(CURRENT_TIMEZONE),
                                            discussion_group_id=group_id)
            AnnouncementsRepository.add_new_announcement(new_announcement)
            logging.info(f"New announcement posted in : {group_id} by {announcement_data['author']}")
        except exc.SQLAlchemyError:
            logging.error(f"Announcement failed to be posted in : {group_id} by {announcement_data['author']}")
            return make_response(jsonify({"error": "Could not add new announcement"}), 503)
        except KeyError:
            return make_response(jsonify({"error": "Announcement structure incomplete"}), 400)

        return make_response(jsonify({"message": "New announcement posted successfully"}), 202)

    @staticmethod
    @token_required
    def patch(current_user):
        if not current_user.teaching:
            return make_response(jsonify({'message': 'User must be a teacher for this operation.'}), 403)
        group_id = request.path.split('/')[2]
        announcement_id = request.args.get('id')
        updated_announcement_data = request.get_json()

        try:
            AnnouncementsRepository.update_announcement(announcement_id, updated_announcement_data)
        except exc.SQLAlchemyError:
            logging.error(f"Announcement failed to be updated in : {group_id}")
            return make_response(jsonify({"error": "Could not add new announcement"}), 503)

        return make_response(jsonify({"message": "Announcement updated successfully"}), 200)

    @staticmethod
    @token_required
    def delete(current_user):
        if not current_user.teaching:
            return make_response(jsonify({'message': 'User must be a teacher for this operation.'}), 403)
        announcement_id = request.args.get('id')
        try:
            AnnouncementsRepository.delete_announcement(announcement_id)
        except exc.SQLAlchemyError:
            logging.error(f"Failed to delete announcement with id : {announcement_id}")
            return make_response(jsonify({"error": f"Failed to delete announcement for id {announcement_id}."}), 503)

        return make_response(jsonify({"message": "Announcement deleted successfully"}), 200)
