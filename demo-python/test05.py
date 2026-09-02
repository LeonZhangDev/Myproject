def add_user(name, user=[]):
    user.append(name)
    return user

print(add_user("Alice"))
print(add_user("Bob"))
print(add_user("Charlie", ["David"]))


def add_user1(name, user1=None):
    if user1 is None:
        user1 = []
    user1.append(name)
    return user1

user = ["David"]

print(add_user1("Alice", user))
print(add_user1("Bob",  user))
