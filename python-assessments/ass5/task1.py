from abc import ABC, abstractmethod


class Person(ABC):
    """Abstract base class representing a person."""

    def __init__(self, name, age, gender, address):
        super().__init__()  # cooperative inheritance
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address

    def __str__(self):
        """Return the person's details in the required format."""
        return (
            f"Name: {self.name}, Age: {self.age}, "
            f"Gender: {self.gender}, Address: {self.address}"
        )

    def greet(self, other_person):
        """Greet another Person object."""
        print(f"Hello {other_person.name}! My name is {self.name}.")

    @abstractmethod
    def introduce(self):
        """Introduce the person. Must be implemented by child classes."""
        pass

    @staticmethod
    def is_adult(age):
        """Return True if age is 18 or above, otherwise False."""
        return age >= 18


class Student(Person):
    """Concrete child class of Person."""

    def __init__(self, name, age, gender, address, college):
        super().__init__(name, age, gender, address)  # cooperative inheritance
        self.college = college

    def introduce(self):
        """Implement the abstract introduce method."""
        print(
            f"Hello, my name is {self.name}. "
            f"I am a student at {self.college}."
        )


if __name__ == "__main__":
    # Create Student objects.
    person1 = Student("Garv", 21, "Male", "Jaipur", "PIET")
    person2 = Student("Rahul", 20, "Male", "Delhi", "ABC College")

    # Demonstrate __str__().
    print(person1)

    # Demonstrate greet().
    person1.greet(person2)

    # Demonstrate introduce().
    person1.introduce()

    # Demonstrate the static method is_adult().
    print(Person.is_adult(21))
    print(Person.is_adult(16))