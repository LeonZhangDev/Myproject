class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."
    
user1 = User("Alice", 30)
print(user1.greet())

class User1:
    count = 0
    def __init__(self, name):
        self.name = name
        User1.count += 1

a = User1("Alice")
b = User1("Bob")
c = User1("Charlie")
print(User1.count)