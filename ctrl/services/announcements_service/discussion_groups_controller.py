from flask_restful import Resource
from flask import make_response, jsonify
from repository import DiscussionGroupsMembersRepository, DiscussionGroupsRepository
from services.auth.token_config import token_required


# TODO: check for possibility to upload avatar to GC

class DiscussionGroupsController(Resource):
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
                "avatar": "",
                # "avatar": "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png"
            })

        return make_response(jsonify({'current_user_groups': current_user_groups_extended}), 200)
