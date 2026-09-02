a = [1,2]
b = [1,2]
print(a == b)
print(a is b)

result = None
if result is None:
    print("result is None")
    
a = [1, 2, 3]
b = a.copy()

b.append(4)
print(a)
print(b)

a = [
    [1, 2],
    [3, 4]
]

b = a.copy()
b[0].append(5)
print(a)
print(b)

a = [1, 2, 3]
b = a

print(a is b)
print(a == b)