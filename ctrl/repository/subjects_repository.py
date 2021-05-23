from typing import List
from sqlalchemy import func
from model import Subject


class SubjectsRepository:
    @staticmethod
    def get_all_subjects() -> List[Subject]:
        """
        :return: a list of all the subjects found in the database
        """
        return Subject.query.all()

    @staticmethod
    def get_subject_by_code(code):
        subject = Subject.query.filter(func.upper(Subject.username) == code.upper()).first()
        return subject if subject else False

    @staticmethod
    def get_subject_for_id(subject_id):
        subject = Subject.query.filter(Subject.id == subject_id).first()
        return subject if subject else False
