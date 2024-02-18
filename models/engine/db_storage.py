#!/usr/bin/python3
"""Define storage engine using MySQL database
"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker, Session
from os import getenv

all_classes = {'State': State, 'City': City,
               'User': User, 'Place': Place,
               'Review': Review, 'Amenity': Amenity}

class DBStorage:
    """
    This class manages the storage for the program using SQLAlchemy
    """
    __engine = None
    __session = None

    def __init__(self):
        """Create SQLAlchemy engine
        """
        # create the engine
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                    format(getenv('HBNB_MYSQL_USER'),
                                           getenv('HBNB_MYSQL_PWD'),
                                           getenv('HBNB_MYSQL_HOST'),
                                           getenv('HBNB_MYSQL_DB')),
                                    pool_pre_ping=True)
        # drops the tables if it the test.
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query and return all objects by class/generally
        Return: dictionary (<class-name>.<object-id>: <obj>)
        """
        my_dict = {}

        # select from the current database using cls as key
        if cls:
            for row in self.__session.query(cls).yield_per(100):
                my_dict[f'{cls.__name__}.{row.id}'] = row
        # if cls=None query all the other classes
        else:
            for key, value in all_classes.items():
                for row in self.__session.query(value).yield_per(100):
                    my_dict[f'{value.__name__}.{row.id}'] = row

        # return dictionary
        return my_dict
    
    def new(self, obj):
        """
        add the object to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session obj if not None
        """
        if obj:
            # find the class in obj
            class_name = all_classes[type(obj).__name__]
            # query the class form the table and delete it
            self.__session.query(class_name).filter(class_name.id == obj.id).delete()

    def reload(self):
        """
        create all tables in the database (feature of SQLAlchemy) 
        """
        # create the session for the current engine
        Base.metadata.create_all(self.__engine)
        # create the database tables
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)

        self.__session = scoped_session(session)

     def close(self):
        """call remove() method on self.__session"""
        self.__session.close()
