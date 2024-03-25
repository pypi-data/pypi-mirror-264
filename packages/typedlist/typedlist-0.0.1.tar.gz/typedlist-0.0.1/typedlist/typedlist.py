from typing import TypeVar

class TypedList(list):
    def __init__(self, type_: TypeVar, *args):
        # Init type value
        self.__type: TypeVar = type_
        super().__init__(*args)

    @property
    def type(self) -> TypeVar:
        return self.__type

    def append(self, value):
        if not isinstance(value, self.__type):
            raise TypeError(f"Only {self.__type.__name__} objects can be appended")
        super().append(value)

    def extend(self, values):
        if not all(isinstance(value, self.__type) for value in values):
            raise TypeError(f"All elements must be {self.__type.__name__} objects")
        super().extend(values)
