#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """ Saves user to the db """
        if email is None or hashed_password is None:
            return None

        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs):
        """ takes in arbitrary keyword arguments and returns the first
        row found in the users table """
        try:
            for key, value in kwargs.items():
                user = self._session.query(User).filter_by(**{key: value})\
                    .one()
                return user
        except NoResultFound:
            raise NoResultFound("No User data!")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query!")

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates user details passed as kwargs """
        user = self.find_user_by(id=user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                    self._session.commit()
                else:
                    raise ValueError("No data match!")
