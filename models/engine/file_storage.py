#!/usr/bin/python3
"""
    file storage module
"""
import json
import os.path as path
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

ac = {"BaseModel": BaseModel, "Amenity": Amenity, "City": City,
      "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage():
    """
    FileStorage class: that serializes and deserializes
    a JSON file to instances
    Attributes:
    ----------
    __file_path: string - path to the JSON file
    __objects: dictionary - empty but will store all objects
    """
    def __init__(self):
        """ """
        self.__file_path = "file.json"
        self.__objects = {}

    def all(self):
        """
        Public method that returns the dictionary __objects
        """
        return (self.__objects)

    def new(self, obj):
        """
        Public method that sets in __objects the obj with key
        """
        c_n = obj.__class__.__name__ + "." + obj.id
        self.__objects[c_n] = obj

    def save(self):
        """
        Public method that serializes __objects to the JSON file
        """
        new_object = {}
        for key, value in self.__objects.items():
            new_object.update({key: value.to_dict()})
        myjson = json.dumps(new_object)
        with open(self.__file_path, "w") as f:
            f.write(myjson)

    def delete(self, obj=None):
        """
        Public method that deletes an instance based on the class
        """
        if obj is not None:
            del self.__objects[obj.__class__.__name__ + '.' + obj.id]
            self.save()

    def reload(self):
        """
        Public method that deserializes the JSON file to __objects
        """
        if path.isfile(self.__file_path):
            with open(self.__file_path, "r") as f:
                jf = json.load(f)
                for key in jf:
                    self.__objects[key] = ac[jf[key]["__class__"]](**jf[key])
