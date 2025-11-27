# app/services/calculation_factory.py

from abc import ABC, abstractmethod
from app.models import CalculationType


# 1) Base operation interface
class BaseOperation(ABC):
    @abstractmethod
    def compute(self, a: float, b: float) -> float:
        """Return the result of the operation."""
        ...


# 2) Concrete operations
class AddOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        return a + b


class SubOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        return a - b


class MultiplyOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        return a * b


class DivideOperation(BaseOperation):
    def compute(self, a: float, b: float) -> float:
        if b == 0:
            # Tests expect this error
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b


# 3) Factory used by tests
class CalculationFactory:
    @staticmethod
    def get_operation(calc_type: CalculationType) -> BaseOperation:
        """
        Tests call:
        CalculationFactory.get_operation(CalculationType.ADD)
        and expect an object with .compute(a, b)
        """
        if calc_type == CalculationType.ADD:
            return AddOperation()
        elif calc_type == CalculationType.SUB:
            return SubOperation()
        elif calc_type == CalculationType.MULTIPLY:
            return MultiplyOperation()
        elif calc_type == CalculationType.DIVIDE:
            return DivideOperation()
        else:
            raise ValueError(f"Unsupported calculation type: {calc_type}")

    # Backward-compatible alias if you used this name before
    @staticmethod
    def create_operation(calc_type: CalculationType) -> BaseOperation:
        return CalculationFactory.get_operation(calc_type)
