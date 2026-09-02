class User:
    def __init__(self, name:str):
        self.name = name


    def greet(self):
        return f"Hello, my name is {self.name}"
    
user =User("tom")
print(user.greet())

class User1:
    count = 1
    def __init__(self, name:str):
        self.name = name
        User1.count += 1

u1 = User1("tom")
u2 = User1("jack")
print(User1.count)