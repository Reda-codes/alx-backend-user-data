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

    def create_session(self, email: str) -> str:
        """ Method to create a session ID """
        try:
            userID = self._db.find_user_by(email=email).id
            sessionID = _generate_uuid()
            self._db.update_user(userID, session_id=sessionID)
            return self._db.find_user_by(email=email).session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Method to gets a User from a session ID """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, InvalidRequestError) as e:
            return None

    def destroy_session(self, user_id: int):
        """ Method that updates the user’s session ID to None """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ Method to reset a user password token """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except (Exception, NoResultFound, InvalidRequestError) as e:
            raise ValueError

    def update_password(self, reset_token: str, password: str):
        """ Method to update a users's password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password)
        except (Exception, NoResultFound, InvalidRequestError) as e:
            raise ValueError
