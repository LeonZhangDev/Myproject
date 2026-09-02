def greet(name,message="Welcome to the platform!"):
    return f"Hello {name}, {message}"

print(greet("Alice"))
print(greet("Bob", "Glad to have you here!"))

def add(*args):
    total = 0
    
    for num in args:
        total += num
    
    return total

print(add(1, 2, 3, 4 ,5),"hi")

def show_user(**kwargs):
    print(kwargs)
    
show_user(name="Alice", age=30, city="New York")