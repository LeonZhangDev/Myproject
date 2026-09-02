try:
    num = int("adfa")
    
except ValueError as e:
    print("ValueError:", e)

finally:
    print("This block will always execute.")
    
class AgeError(Exception):
    pass   

def check_age(age:int):
    if age < 0:
        raise AgeError("年龄不能小于0")

try:
    check_age(-5)
except AgeError as e:
    print("AgeError:", e)