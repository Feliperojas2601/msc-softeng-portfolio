from functools import lru_cache

from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.calculate_use_case import CalculateUseCase


@lru_cache()
def build_calculate_use_case() -> BaseUseCase:
    """Get calculate use case."""
    return CalculateUseCase()
