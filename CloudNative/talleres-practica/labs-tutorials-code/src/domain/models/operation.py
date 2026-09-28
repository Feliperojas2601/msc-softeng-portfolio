from dataclasses import dataclass
from enum import Enum

from errors import InvalidOperationError, ValidationError


class Sign(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"

    @classmethod
    def values(cls):
        return [item.value for item in Sign]


@dataclass
class Operation:
    number1: float
    number2: float
    sign: Sign

    def __post_init__(self):
        if not isinstance(self.number1, (int, float)):
            raise ValidationError("number1 is mandatory.")
        if not isinstance(self.number2, (int, float)):
            raise ValidationError("number2 is mandatory.")
        if self.sign is None:
            raise ValidationError("sign is mandatory.")
        if self.sign not in Sign.values():
            raise InvalidOperationError(
                f"'{self.sign}' is not a supported operation. Supported operations are: {Sign.values()}"
            )
        self.sign = Sign(self.sign)
