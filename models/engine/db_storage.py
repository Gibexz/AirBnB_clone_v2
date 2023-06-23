#!/usr/bin/python3
import MySQLdb
from sqlalchemy import create_engine
from urllib.parse import quote
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session, backref, relationship
from models.base_model import Base

from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class DBStorage():
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", default = 'localhost')
        data_base = getenv("HBNB_MYSQL_DB")
        escaped_password = quote(password)
        db_url = f"mysql+mysqldb://{user}:{escaped_password}@{host}/{data_base}"
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):

        objDict = {}
        if cls:
            if isinstance(cls, str):
                cls = globals()[cls]

            query = self.__session.query(cls).all()
            for obj in query:
                key = f"{type(obj).__name__}.{obj.id}"
                objDict[key] = obj
        else:
            cls_list = [State, City, User, Place, Review, Amenity]
            for clas in cls_list:
                query = self.__session.query(clas).all()
                for obj in query:
                    key = f"{type(obj).__name__}.{obj.id}"
                    objDict[key] = obj
        return objDict

    def new(self, obj):
        """ adds the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ save/commit changes """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Reload """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()
