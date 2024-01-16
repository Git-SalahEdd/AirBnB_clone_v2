#!/usr/bin/python3
"""This is the place class"""

from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import environ

Base = declarative_base()

class Place(BaseModel, Base):
    """This class defines place
    Attributes:
        city_id: city id (string, 60 chars, not null, foreign key to cities.id)
        user_id: user id (string, 60 chars, not null, foreign key to users.id)
        name: name (string, 128 chars, not null)
        description: description (string, 1024 chars, nullable)
        number_rooms: number of rooms (integer, not null, default: 0)
        number_bathrooms: number of bathrooms (integer, not null, default: 0)
        max_guest: maximum number of guests (integer, not null, default: 0)
        price_by_night: price by night (integer, not null, default: 0)
        latitude: latitude (float, nullable)
        longitude: longitude (float, nullable)
        user: relationship with User object
    """
    __tablename__ = 'places'

    city_id = Column(String(60), nullable=False, ForeignKey('cities.id'))
    user_id = Column(String(60), nullable=False, ForeignKey('users.id'))
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Relationship with User object
    user = relationship('User', backref='places')
    
    if environ['HBNB_TYPE_STORAGE'] == 'db':
        reviews = relationship('Review', cascade='all, delete', backref='place')
    else:
        @property
        def reviews(self):
            """
            getter method that
            returns the list of Review instances with place_id
            equals to the current Place.id
            """
            from models import storage
            from models.review import Review
            # get the dict of all the reviews
            review_dict = storage.all()
            review_list = []
            # loop though the reviews, map those that correspond to current
            # place_id
            for review in review_dict.values():
                if Review.place_id == self.id:
                    review_list.append(review)
            # return list of corressponding reviews
            return review_list
