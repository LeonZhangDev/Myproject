def numbers():
    for i in range(5):
        yield i

g =numbers()
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))


def logger(func):
    
    def wrapper():
        print("start")
        func()
        print("end")
    return wrapper
@logger
def hello():
    print("hello")
    
new_func = logger(hello)
hello()
new_func()

with open("test.txt","w", encoding="utf-8") as f:
    f.write("ni hao")