class Citation(object):
    """
    This class takes arbitrary attributes and stores the assigned data in a dictionary.
    Every attribute is interpreted as a property
    and the getter, setter and deleter methods manipulate the _data dictionary.
    The attributes can also be predefined in the constructor using keyword arguments.
    """

    def __init__(self, **kwargs):
        self._data = kwargs
        for name, value in kwargs.items():
            setattr(self, name, value)

    def get_data(self):
        return self._data

    def __getattr__(self, name: str) -> any:
        @property
        def method():
            return self._data[name]

        @method.setter
        def method(value):
            self._data[name] = value

        @method.deleter
        def method():
            self._data.pop(name)

        if name in self._data:
            return method
        else:
            return None
