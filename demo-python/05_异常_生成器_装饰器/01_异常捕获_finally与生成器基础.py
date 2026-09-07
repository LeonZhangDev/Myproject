try:
    10/0
except ZeroDivisionError:
    print("Cannot divide by zero.")
    
print("Program continues after exception handling.")

try:
    num = int("abc")
except ValueError:
    print("Invalid input. Please enter a valid integer.")
finally:
    print("end")
    
def numbers():
    yield 1
    yield 2
    yield 3
    
result = numbers()
print(next(result))
print(next(result))
print(next(result))

