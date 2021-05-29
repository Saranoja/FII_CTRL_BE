from typing import List
from model import Assignment
from sqlalchemy import exc
from database_connection import db


class AssignmentsRepository:
    @staticmethod
    def get_all_assignments() -> List[Assignment]:
        """
        :return: a list of all the assignments found in the database
        """
        return Assignment.query.all()

    @staticmethod
    def get_assignment_with_id(assignment_id: int) -> Assignment:
        f"""
        :return: the assignment with id {assignment_id}
        """
        return Assignment.query.filter(Assignment.id == assignment_id).first()

    @staticmethod
    def get_assignments_for_group(group_id: int):
        f"""
        :return: a list of all the assignments found in the database corresponding to the group with {group_id}
        """
        return Assignment.query.filter(Assignment.discussion_group_id == group_id).all()

    @staticmethod
    def get_assignments_by_author(author_id: int):
        f"""
            :return: a list of all the assignments posted by the author with {author_id}
            """
        return Assignment.query.filter(Assignment.author_id == author_id).all()

    @staticmethod
    def add_new_assignment(assignment: Assignment):
        try:
            db.session.add(assignment)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise exc.SQLAlchemyError

    @staticmethod
    def update_assignment(assignment_id: int, updated_assignment: dict):
        try:
            target_assignment = Assignment.query.filter(Assignment.id == assignment_id)
            target_assignment.update(updated_assignment)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise exc.SQLAlchemyError
        except KeyError:
            raise KeyError

    @staticmethod
    def delete_assignment(assignment_id: int):
        try:
            target_assignment = Assignment.query.filter(Assignment.id == assignment_id).first()
            db.session.delete(target_assignment)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise exc.SQLAlchemyError
