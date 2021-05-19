from typing import List
from sqlalchemy import func
from model import User


class UsersRepository:
    @staticmethod
    def get_all_users() -> List[User]:
        """
        :return: a list of all the  users found in the database
        """
        return User.query.all()

    @staticmethod
    def is_user_valid(id):
        user = User.query.filter(User.id == id).first()
        return user if user else False

    @staticmethod
    def get_user_by_username(username):
        user = User.query.filter(func.lower(User.username) == username.lower()).first()
        return user if user else False

    @staticmethod
    def get_user_for_id(user_id):
        user = User.query.filter(User.id == user_id).first()
        return user if user else False
