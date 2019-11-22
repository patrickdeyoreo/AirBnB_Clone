#!/usr/bin/python3
"""
Provides a class 'FileStorage' to facilitate persistence of models
"""
import models
from json import dump, load


class FileStorage:
    """
    Facilitates model persistence via JSON serialization / deserialization
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Get the dictionary of existing model instances
        """
        return self.__class__.__objects

    def new(self, obj):
        """
        Add a model to the dictionary of existing model instances
        """
        key = '{}.{}'.format(obj.__class__.__name__, obj.id)
        self.__class__.__objects[key] = obj

    def save(self):
        """
        Save the dictionary of existing model instances to the filesystem
        """
        with open(self.__class__.__file_path, "w") as ofile:
            objects = {key: val.to_dict() for
                       key, val in self.__class__.__objects.items()}
            dump(objects, ofile)

    def reload(self):
        """
        Load the dictionary of saved model instances from the filesystem
        """
        try:
            with open(self.__class__.__file_path, "r") as ifile:
                objects = load(ifile)
                for key, val in objects.items():
                    cls = models.getmodel(key.split(".")[0])
                    if cls:
                        self.__class__.__objects[key] = cls(**val)
        except FileNotFoundError:
            pass
