#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy import (Column, String,
                         ForeignKey, Float,
                         Integer, Table)
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
from models.review import Review
from models.amenity import Amenity

linked_table = Table('place_amenity', Base.metadata,
                     Column('place_id', String(60),
                            ForeignKey('places.id'),
                            primary_key=True, nullable=False),
                     Column('amenity_id', String(60),
                            ForeignKey('amenities.id'),
                            primary_key=True, nullable=False)) 


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'
    id = Column(String(60), primary_key=True)
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """Getter for reviews"""
            all_reviews = list(models.storage.all(Review).values())
            review_list = [review for review in all_reviews if review.place_id == self.id]
            return review_list

        @property
        def amenities(self):
            """Getter for amenities"""
            all_amenities = list(models.storage.all(Amenity).values())
            amenity_list = [amenity for amenity in all_amenities if amenity.id in self.amenity_ids]
            return amenity_list
        
        @amenities.setter
        def amenities(self, value):
            """Setter for amenities"""
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
