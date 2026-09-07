def numbers():
    print("Start of generator")
    yield 1
    print("continue after first yield")
    yield 2
    
g = numbers()

print("A")
print(next(g))
print("B")
print(next(g))