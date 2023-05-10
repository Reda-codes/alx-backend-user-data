#!/usr/bin/env python3
""" Auth module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid


def _hash_password(password: str) -> bytes:
    """ Method that takes string arguments and returns bytes """
    salt = b'$2b$12$eUDdeuBtrD41c8dXvzh95eh'
    return bcrypt.hashpw(password.encode(), salt)


def _generate_uuid() -> str:
    """ function that returns a new UUID string """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Method to regester a new user """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """ Method to check for valid login credentials """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = _hash_password(password)
            if user.hashed_password == hashed_password:
                return True
            else:
                return False
        except (NoResultFound, InvalidRequestError) as e:
            return False
