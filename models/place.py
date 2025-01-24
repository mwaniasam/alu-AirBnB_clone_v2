#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity

class Place(BaseModel, Base):    
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=True)
    number_bathrooms = Column(Integer, nullable=True)
    max_guest = Column(Integer, nullable=True)
    price_by_night = Column(Integer, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = Column(String(60), ForeignKey('amenities.id'), nullable=True)
    reviews = relationship("Review", backref="place", cascade="all, delete")    
    amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)
    place_amenities = relationship("PlaceAmenity", backref="place", cascade="all, delete")

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """ Getter attribute that returns the list of Review instances """
            from models import storage
            all_reviews = list(models.storage.all(Review).values())
            review_list = [r for r in all_reviews if r.place_id == self.id]
            return review_list
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
