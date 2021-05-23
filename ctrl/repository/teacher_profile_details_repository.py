from model import TeacherProfileDetails
from sqlalchemy import exc
from database_connection import db


class TeachersProfileDetailsRepository:
    @staticmethod
    def get_details_for_teacher(teacher_id):
        return TeacherProfileDetails.query.filter(TeacherProfileDetails.user_id == teacher_id).first()

    @staticmethod
    def update_details(teacher_id: int, updated_details: dict):
        try:
            current_details = TeacherProfileDetails.query.filter(TeacherProfileDetails.user_id == teacher_id)
            current_details.update(updated_details)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise exc.SQLAlchemyError
        except KeyError:
            raise KeyError
