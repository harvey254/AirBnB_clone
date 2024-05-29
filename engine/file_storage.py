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


hbnb_dict = {
        "User": User,
        "City": City,
        "State": State,
        "Basemodel": BaseModel,
        "Review": Review,
        "Amenity": Amenity,
        "Place": Place
        }

class FileStorage:
    """The file storage engine class that serializes and deserializes instances to a JSON file
    """
    __file_path = "file.json"
    __objects = {}

    def all(self)
        """ returns the dictionary __objects """
        return self.__objects

    def new(self, obj)
        """ sets in __objects the obj with key <obj class name>.id """
        hbnb = obj.__class__.__name__ + "." + obj.id
        self.__objects[hbnb] = obj

    def save(self)
        """ serializes __objects to the JSON file (path: __file_path) """
         new_object = {}
        for key, value in self.__objects.items():
            new_object.update({key: value.to_dict()})
        myjson = json.dumps(new_object)
        with open(self.__file_path, "w") as f:
            f.write(myjson)

    def reload(self)
        """ deserializes the JSON file to __objects (only if the JSON file (__file_path) exists """
        if path.isfile(self.__file_path):
            with open(self.__file_path, "r") as f:
                json_file = json.load(f)
                for key in json_file:
                    self.__objects[key] = hbnb[json_file[key]["__class__"]](**json_file[key])

