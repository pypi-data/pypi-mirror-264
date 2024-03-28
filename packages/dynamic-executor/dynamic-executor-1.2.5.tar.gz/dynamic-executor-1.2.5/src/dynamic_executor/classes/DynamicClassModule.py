from .DynamicClassCreator import DynamicClassCreator


class DynamicClass(metaclass=DynamicClassCreator):
    """
    Abstract class that is to be extended in order to implement instance tracking polity
    that allows instance runtime updates.
    """
