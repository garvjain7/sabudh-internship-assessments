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


class Teacher(Employee):
    counter = 0  # tracks number of currently alive Teacher objects

    def __init__(self, name, age, gender, address, salary, subjects=None):
        super().__init__(name, age, gender, address, salary)  # cooperative inheritance
        Teacher.counter += 1
        self.__teacher_id = f"TEC{Teacher.counter:02d}"  # auto-generated, private
        self.subjects = subjects if subjects is not None else []

    def __del__(self):
        Teacher.counter -= 1
        super().__del__()  # cooperative: also decrement Employee.counter

    @property
    def teacher_count(self):
        return Teacher.counter

    @property
    def teacher_id(self):
        return self.__teacher_id  # getter only, no setter

    def add_subject(self, subject):
        self.subjects.append(subject)

    def remove_subject(self, subject):
        if subject in self.subjects:
            self.subjects.remove(subject)

    def introduce(self):
        return f"My ID is {self.__teacher_id} and I teach: {', '.join(self.subjects)}"

    @property
    def employee_id(self):
        # teachers use teacher_id instead; block access with dynamic class name
        raise AttributeError(f"{self.__class__.__name__} object has no attribute 'employee_id'")


if __name__ == "__main__":
    t1 = Teacher("Anita", 35, "Female", "Jaipur", 70000, ["Mathematics", "Physics"])
    t2 = Teacher("Ravi", 40, "Male", "Delhi", 75000)

    print(t1.introduce())
    print(t1.teacher_id, t2.teacher_id)
    print("Active teachers:", t1.teacher_count)

    t2.add_subject("Chemistry")
    t2.add_subject("Biology")
    t2.remove_subject("Chemistry")
    print(t2.introduce())

    try:
        print(t1.employee_id)
    except AttributeError as e:
        print(e)

    del t2
    print("Active teachers after deletion:", t1.teacher_count)