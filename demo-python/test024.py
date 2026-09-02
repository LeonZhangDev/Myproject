from typing import Annotated, Any
from pydantic import BaseModel, BeforeValidator,PlainValidator


def ensure_list(value: Any) -> Any:
    if not isinstance(value, list):
        return [value]
    else:
        return value


class Model(BaseModel):
    numbers: Annotated[list[int], BeforeValidator(ensure_list)]
    
print(Model(numbers=[2]))

def val_number(value: Any) -> Any:
    if isinstance(value, int):
        return value * 2
    else:
        return value


class Model(BaseModel):
    number: Annotated[int, PlainValidator(val_number)]
    
print(Model(number=4))