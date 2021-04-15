from typing import List
from model import Reference
from sqlalchemy import exc
from database_connection import db


class ReferencesRepository:
    @staticmethod
    def get_all_resources() -> List[Reference]:
        """
        :return: a list of all the  resources found in the database
        """
        return Reference.query.all()

    @staticmethod
    def does_resource_exist(hash):
        resource = Reference.query.filter(Reference.hash == hash).first()
        return resource if resource else False

    @staticmethod
    def add_new_resource(resource):
        try:
            db.session.add(resource)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
