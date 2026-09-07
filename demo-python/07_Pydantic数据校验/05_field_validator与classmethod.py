from pydantic import BaseModel, field_validator, model_validator
from typing import Any

class Model(BaseModel):
    f1: str
    f2: str

    @field_validator('f1', 'f2', mode='before')
    @classmethod
    def capitalize(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.capitalize()

        return value
m = Model(
    f1="hello",
    f2="wORLD"
)

print(m)

class Person:
    name = "Tom"

    def test1(self):
        print(self)

    @classmethod
    def test2(cls):
        print(cls)

p = Person()

p.test1()
p.test2()