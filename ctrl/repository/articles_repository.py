from typing import List
from model import Article
from sqlalchemy import exc
from database_connection import db


class ArticlesRepository:
    @staticmethod
    def get_all_resources() -> List[Article]:
        """
        :return: a list of all the  resources found in the database
        """
        return Article.query.all()

    @staticmethod
    def does_resource_exist(hash):
        resource = Article.query.filter(Article.hash == hash).all()
        return resource if resource else False

    @staticmethod
    def add_new_resource(resource):
        try:
            db.session.add(resource)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
