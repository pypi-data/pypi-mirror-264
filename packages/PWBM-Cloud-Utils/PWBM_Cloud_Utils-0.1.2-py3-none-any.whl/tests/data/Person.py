# for pickle testing
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name and self.age == other.age
