class Citation:
    """
    This class takes arbitrary attributes and stores the assigned data in the class dictionary.
    Every attribute is to be assigned as a property.
    The attributes can also be predefined in the constructor using keyword arguments.
    """

    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def get_data(self):
        return self.__dict__
