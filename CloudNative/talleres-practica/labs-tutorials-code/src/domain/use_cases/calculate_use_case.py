from domain.models.operation import Operation, Sign
from domain.use_cases.base_use_case import BaseUseCase
from errors import DivisionByZeroError


class CalculateUseCase(BaseUseCase):
    """Calculate result use case"""

    def add(self, first: float, second: float) -> float:
        """Returns the sum of both numbers."""
        return first + second

    def substract(self, first: float, second: float) -> float:
        """Returns the substraction of both numbers."""
        return first - second

    def multiply(self, first: float, second: float) -> float:
        """Returns the multiplication of both numbers."""
        return first * second

    def divide(self, first: float, second: float) -> float:
        """Returns the division of both numbers."""
        if second == 0:
            raise DivisionByZeroError("Division by zero is not allowed")
        return first / second

    def execute(self, operation: Operation) -> float:
        """Calculate the result of the operation"""
        if operation.sign == Sign.ADD:
            return self.add(operation.number1, operation.number2)
        if operation.sign == Sign.DIVIDE:
            return self.divide(operation.number1, operation.number2)
        if operation.sign == Sign.MULTIPLY:
            return self.multiply(operation.number1, operation.number2)
        if operation.sign == Sign.SUBTRACT:
            return self.substract(operation.number1, operation.number2)
