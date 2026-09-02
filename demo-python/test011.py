# import copy
# a = [1,2]
# b = a
# c = copy.deepcopy(a)
# a.append(3)
# print(a)
# print(b)
# print(c)

import copy

a = [
    [1, 2],
    [3, 4]
]

b = a.copy()          # 浅拷贝
c = copy.deepcopy(a)  # 深拷贝

a[0].append(100)

print("a =", a)
print("b =", b)
print("c =", c)
print(a is b)       # False
print(a == b)       # False
print(a[0] is b[0]) # True
print(a[0] == b[0]) # True
print(a is c)       # False
print(a[0] is c[0]) # False