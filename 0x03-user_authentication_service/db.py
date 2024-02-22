#!/usr/bin/env python3
"""DB module
    Creates a connection to a db
    Has db ops
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Type
from user import User
from sqlalchemy.exc import InvalidRequestError, NoResultFound


from user import Base


class DB:
    """DB class
    Defined db operations. CRUD
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        creates a db session
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Saves a user to the db """
        if email is None or hashed_password is None:
            return None

        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Returns the first Row in users table as filtered by input args """
        try:
            for key, value in kwargs.items():
                query = self.__session.query(User).filter_by(**{key: value})
                user = query.one()
                return user
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id: int = None, **kwargs) -> None:
        """ Uses find_user_by to locate & update user attributes """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            return None

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()
