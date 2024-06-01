#!/usr/bin/python3
"""An interactive command interpreter for HBNB."""

import cmd
import re
import models
from models.base_model import BaseModel
from models import storage
import json
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class_registry = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "Amenity": Amenity,
    "City": City,
    "Review": Review,
    "State": State
}


class HBNBCommand(cmd.Cmd):
    """ HBNB class odule """

    prompt = '(hbnb) '

    def do_EOF(self, line):
        """Handles EOF to exit the command interpreter"""
        print("")
        return True

    def do_quit(self, line):
        """Handles the quit command to exit the command interpreter"""
        print("Goodbye!")
        return True

    def help_quit(self):
        """Provides help information for the quit command"""
        print("Quit command to exit the program")

    def emptyline(self):
        """Overrides the default behavior of repeating the last command"""
        return False

    def do_create(self, line):
        """Creates a new instance of a specified class"""
        if line:
            class_type = globals().get(line, None)
            if class_type:
                instance = class_type()
                instance.save()
                print(instance.id)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_show(self, line):
        """Displays the string representation of an instance"""
        args = line.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in class_registry:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key in storage.all():
                print(storage.all()[key])
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on class name and id"""
        args = line.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in class_registry:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key in storage.all():
                del storage.all()[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, line):
        """Displays all instances"""
        objects = []
        if not line:
            objects = [str(obj) for obj in storage.all().values()]
        else:
            if line not in class_registry:
                print("** class doesn't exist **")
                return
            objects = [str(obj) for obj in storage.all().values()
                       if obj.__class__.__name__ == line]
        print(objects)

    def do_update(self, line):
        """Updates an instance by adding or updating an attribute"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in class_registry:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        setattr(storage.all()[key], args[2], args[3])
        storage.save()

    def do_count(self, line):
        """Counts the number of instances of a class"""
        if line not in class_registry:
            print("** class doesn't exist **")
            return
        count = sum(1 for obj in storage.all().values()
                    if obj.__class__.__name__ == line)
        print(count)

    def default(self, line):
        """Handles unknown commands by
        interpreting them as <class>.<method>(<args>)
        """
        if not line:
            return

        match = re.match(r"^([A-Za-z]+)\.([a-z]+)\(([^)]*)\)$", line)
        if not match:
            super().default(line)
            return

        class_name, method_name, args = match.groups()
        args = re.findall(r'"(.*?)"', args)

        if method_name == 'all':
            return self.do_all(class_name)
        if method_name == 'count':
            return self.do_count(class_name)
        if method_name == 'show' and args:
            return self.do_show(f"{class_name} {args[0]}")
        if method_name == 'destroy' and args:
            return self.do_destroy(f"{class_name} {args[0]}")
        if method_name == 'update':
            if len(args) == 3:
                return self.do_update(f"{class_name}{args[0]} {args[1]} {args[2]}")
            if len(args) == 2:
                return self.do_update(f"{class_name} {args[0]} {args[1]}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
