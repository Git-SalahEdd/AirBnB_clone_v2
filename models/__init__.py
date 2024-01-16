#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import environ
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

storage_type = environ.get('HBNB_TYPE_STORAGE', 'file')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
