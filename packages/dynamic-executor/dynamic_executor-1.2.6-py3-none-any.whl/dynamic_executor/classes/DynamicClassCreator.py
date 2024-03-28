from typing import List


class DynamicClassCreator(type):
    """
    Metaclass that makes classes track their instances and stores them.

    Created to update methods and class fields of dynamic class instances as the classes change.
    """

    created_classes: List["DynamicClassCreator"] = []

    def __new__(metacls, name, bases, namespace):
        new_class = super().__new__(metacls, name, bases, namespace)
        metacls.created_classes.append(new_class)
        new_class._instances = []
        new_class.__new__ = new_wrapper(new_class.__new__)
        return new_class


def new_wrapper(new):
    """Class __new__ method wrapper that ensures that the new instance is stored in _instances list of a dynamic class."""

    def wrapper(cls, *args, **kwargs):
        new_instance = new(cls)
        if new_instance not in cls._instances:
            cls._instances.append(new_instance)
        return new_instance

    return wrapper
