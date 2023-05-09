"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User, Base
from typing import Any, Dict, Optional


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Method add_user to add a new user to the database """
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs: Dict[str, Any]) -> Optional[User]:
        """ Method find_user_by to get a user based on a key and a value """
        key = list(kwargs.items())[0][0]
        value = list(kwargs.items())[0][1]
        if key not in dir(User):
            raise InvalidRequestError
        session = self._session
        user = session.query(User).filter(getattr(User, key) == value).first()
        if user:
            return user
        else:
            raise NoResultFound

    def update_user(self,
                    user_id: str,
                    **kwargso: Dict[str, Any]) -> Optional[None]:
        """ Method update_user to Update an existing user """
        session = self._session
        user = session.query(User).filter(User.id == user_id)
        if user:
            for key, value in kwargs.items():
                if key in dir(User):
                    user.update({key: value})
                else:
                    raise ValueError
        return None
