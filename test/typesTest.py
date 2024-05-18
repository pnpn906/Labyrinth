from uuid import uuid4

class User:
    def __init__(self,**kwargs):
        self.name = kwargs["name"]
        self.surname = kwargs["surname"]

class Admin(User):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.root = kwargs["root"]


typeList = (User, Admin)

for type in typeList:
    item = type(name=uuid4(), surname=uuid4(), root=uuid4())
    print(f"Type: {type.__name__}")
    print(f"Name: {item.name}")
    print()

sample = {"name": "test23"}
print(sample.get("surname", "NONE"))