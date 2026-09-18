from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name, age, gender, address):
        super().__init__()  # cooperative inheritance
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address

    def __str__(self):
        return (
            f"Name: {self.name}, Age: {self.age}, "
            f"Gender: {self.gender}, Address: {self.address}"
        )

    def greet(self, other_person):
        print(f"Hello {other_person.name}! My name is {self.name}.")

    @abstractmethod
    def introduce(self):
        pass

    @staticmethod
    def is_adult(age):
        return age >= 18


class Employee(Person):
    counter = 0  # tracks number of currently alive Employee objects

    def __init__(self, name, age, gender, address, salary):
        super().__init__(name, age, gender, address)  # cooperative inheritance
        Employee.counter += 1
        self.__employee_id = f"EMP{Employee.counter:02d}"  # auto-generated, private
        self._salary = salary  # protected

    def __del__(self):
        Employee.counter -= 1

    @property
    def employee_count(self):
        return Employee.counter

    @property
    def employee_id(self):
        return self.__employee_id  # getter only, no setter

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        self._salary = value

    def increase_salary(self, amount):
        self._salary += amount

    def decrease_salary(self, amount):
        self._salary -= amount

    def introduce(self):
        print(f"Hello, my name is {self.name} and I work as an employee.")


if __name__ == "__main__":
    e1 = Employee("John", 30, "Male", "Jaipur", 50000)
    e2 = Employee("Priya", 28, "Female", "Delhi", 60000)

    e1.introduce()
    print(e1.employee_id, e2.employee_id)
    print("Active employees:", e1.employee_count)

    e1.increase_salary(5000)
    e1.decrease_salary(2000)
    print("Updated salary:", e1.salary)

    del e2
    print("Active employees after deletion:", e1.employee_count)