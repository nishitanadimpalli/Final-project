import types

from app.models import CalculationType
from app.services.stats import summarize_calculations


def make_calc(a, b, calc_type):
    obj = types.SimpleNamespace()
    obj.a = a
    obj.b = b
    obj.type = calc_type
    return obj


def test_summarize_calculations_basic():
    calcs = [
        make_calc(1, 2, CalculationType.ADD),
        make_calc(3, 4, CalculationType.ADD),
        make_calc(5, 6, CalculationType.SUB),
    ]

    stats = summarize_calculations(calcs)

    assert stats["total_calculations"] == 3
    assert stats["add_count"] == 2
    assert stats["sub_count"] == 1
    assert stats["multiply_count"] == 0
    assert stats["divide_count"] == 0
    assert stats["avg_a"] == (1 + 3 + 5) / 3
    assert stats["avg_b"] == (2 + 4 + 6) / 3


def test_summarize_calculations_empty():
    stats = summarize_calculations([])

    assert stats["total_calculations"] == 0
    assert stats["add_count"] == 0
    assert stats["sub_count"] == 0
    assert stats["multiply_count"] == 0
    assert stats["divide_count"] == 0
    assert stats["avg_a"] is None
    assert stats["avg_b"] is None
