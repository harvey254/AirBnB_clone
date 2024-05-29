#!/usr/bin/python3
""" defines all common attributes/methods for other classes: """

from datetime import datetime
import models
import uuid


class BaseModel:
    """ Base class for all models """
    def __init__(self, *args, **kwargs):
        """ Constructor class
         Attributes
        ----------
        *args: list of arguments
        **kwargs: dictionary of arguments
        """
    if (kwargs):
        for key, value in kwargs.items():
            if key == 'id':
                self.id = value
            elif key == 'created_at':
                self.created_at = datetime.strptime(value,
                                                    '%Y-%m-%dT%H:%M:%S.%f')
            elif key == 'updated_at':
                self.updated_at = datetime.strptime(value,
                                                    '%Y-%m-%dT%H:%M:%S.%f')
            else:
                if (key != '__class__'):
                    setattr(self, key, value)
    else:
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        models.storage.new(self)

    def to_dict(self):
        """Returns a dictionary that contains all values of the instance"""
        my_dict = dict()
        my_dict['__class__'] = self.__class__.__name__
        for key, value in self.__dict__.items():
            if key in ('created_at', 'updated_at'):
                my_dict[key] = value.isoformat()
            else:
                my_dict[key] = value
        return my_dict

    def save(self):
        """Updates the public instance attribute updated_at
        with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def __str__(self):
        """Returns a readable string representation of BaseModel instances"""
        className = self.__class__.__name__
        return "[{}] ({}) {}".format(className, self.id, self.__dict__)

    def delete(self):
        """Method to deletes an instance based on the class name"""
        models.storage.delete(self)
