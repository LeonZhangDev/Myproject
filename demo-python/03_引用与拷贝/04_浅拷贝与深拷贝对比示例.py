a = [1, 2, 3]
b = a.copy()
b.append(4)
print(a)
print(b)

a=[[1,2],[3,4]]
b=a.copy()
b[0].append(100)
print(a)
print(b)
import copy
a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)
b[0].append(100)
print(a)
print(b)