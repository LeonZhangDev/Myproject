from typing import Annotated, Any
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    WrapValidator,
    ValidatorFunctionWrapHandler,
)

def truncate(
    value: Any,
    handler: ValidatorFunctionWrapHandler
) -> str:

    try:
        return handler(value)

    except ValidationError as err:
        if err.errors()[0]['type'] == 'string_too_long':
            print(err.errors()[0]['msg'])
            return handler(value[:5])
        else:
            raise

class Model(BaseModel):
    my_string: Annotated[
        str,
        Field(max_length=5),
        WrapValidator(truncate),
    ]

print(Model(my_string="hello world"))