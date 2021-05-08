from typing import List
from model import TokenBlacklist
from sqlalchemy import exc
from database_connection import db


class TokenBlacklistRepository:
    @staticmethod
    def get_all_tokens() -> List[TokenBlacklist]:
        """
            :return: a list of all the blacklisted tokens found in the database
        """
        return TokenBlacklist.query.all()

    @staticmethod
    def add_new_blacklisted_token(token):
        try:
            db.session.add(token)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()

    @staticmethod
    def is_token_blacklisted(jti):
        token = TokenBlacklist.query.filter(TokenBlacklist.jti == jti).first()
        return True if token else False
