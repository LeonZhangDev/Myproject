# def decorator(func):
#     def wrapper():
#         print("Before the function is called.")
#         func()
#         print("After the function is called.")
#     return wrapper

# @decorator
# def say_hello():
#     print("Hello!")
    
# say_hello()

def decorator(func):

    def wrapper():
        print("执行前")
        func()
        print("执行后")

    return wrapper


def hello():
    print("Hello")


hello1 = decorator(hello)

hello1()