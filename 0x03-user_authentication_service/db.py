#!/usr/bin/env python3
"""DB module
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
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> Type[User]:
        """ Saves a user to the db """
        if email is None or hashed_password is None:
            return None
        
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        
        return new_user

    def find_user_by(self, **kwargs) -> Type[User]:
        """ Returns the first Row in users table as filtered by input args """
        try:
            result = self._session.query(User).filter_by(**kwargs).first()
            if result is None:
                return NoResultFound
            return result
        except InvalidRequestError:
            raise

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
