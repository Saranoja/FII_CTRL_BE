from flask_restful import Resource
from flask import make_response, jsonify
from services.auth.token_config import token_required


class CurrentUser(Resource):
    @staticmethod
    @token_required
    def get(current_user):
        if current_user.teaching:
            current_user_data = {
                'id': current_user.id,
                'first_name': current_user.first_name, 'last_name': current_user.last_name,
                'teaching': current_user.teaching, 'admin': current_user.admin}
        else:
            current_user_data = {
                'id': current_user.id,
                'first_name': current_user.first_name, 'last_name': current_user.last_name,
                'teaching': current_user.teaching, 'year': current_user.year,
                'group': current_user.group, 'admin': current_user.admin
            }

        return make_response(jsonify(current_user_data), 200)
