nums = [1,1,2,2,3,3,4,4,5,5]
result = list(set(nums))
print(result)

words = ["python", "java", "python", "go"]
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)

def greet(name:str ,message:str ="hello")->str:
    return f"{message},{name}"
print(greet("tom"))
print(greet("jack", "hi"))

def add(*args:int)->int:
    return sum(args)
print(add(1,2,3,4,5))

def show_user(**kwargs):
    print(type(kwargs))
    for key, value in kwargs.items():
        print(f"{key}: {value}")
        
show_user(name="tom", age=20, city="beijing")

a = [1,2,3]
b = a
b.append(4)
print(a)
print(b)
