# def test(x):
#     x += 1
    
# a = 5
# test(a)
# print(a)  # 输出 5
# print(a is 5)  # 输出 True
# print(a == 5)  # 输出 True

def test1(x):
    x = x + [3]
    return x
    
a = [1, 2]
a = test1(a)
print(a)
a = test1(a)
a = test1(a)

print(a)

x = 10
def test2():
    x=20
    print(x)
    
test2()

print(x)  # 输出 10

