def outer(x):
    def inner(y):
        return x + y
    return inner

add_10 = outer(1)
print(add_10)  # 输出 15
print(add_10(5))
print(add_10(20))