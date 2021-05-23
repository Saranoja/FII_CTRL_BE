from typing import List
from sqlalchemy import func
from model import User


class UsersRepository:
    @staticmethod
    def get_all_users() -> List[User]:
        """
        :return: a list of all the users found in the database
        """
        return User.query.all()

    @staticmethod
    def get_all_teachers() -> List[User]:
        """
        :return: a list of all the users with the teacher role
        """
        return User.query.filter(User.teaching).all()

    @staticmethod
    def get_all_students() -> List[User]:
        """
        :return: a list of all the users with the student role
        """
        return User.query.filter(User.student).all()

    @staticmethod
    def get_students_from_year_group(_year, _group) -> List[User]:
        f"""
        :return: a list of all the users with the student role who are in the year {_year} and group {_group}
        """
        return User.query.filter(
            User.student and (User.group == _group if _group else True) and (
                User.year == _year if _year else True)).all()

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
