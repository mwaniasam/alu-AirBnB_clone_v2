#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """ Amenity class """
    __tablename__ = 'amenities'
    id = Column(String(60), primary_key=True)
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity", viewonly=True)

    def __init__(self, *args, **kwargs):
        """ Initialize Amenity Object """
        super().__init__(*args, **kwargs)
        if 'name' in kwargs:
            self.name = kwargs['name']
