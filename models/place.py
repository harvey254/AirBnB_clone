#!/usr/bin/python3
""" Place module """

from models.base_model import BaseModel


class Place(BaseModel):
    """ Classrepresentation of  Place """
    user_id = ""
    name = ""
    latitude = 0.0
    longitude = 0.0
    description = ""
    city_id = ""
    room_number = 0
    bathroom_number = 0
    night_price = 0
    maximum_guests = 0
    amenity_ids = []
