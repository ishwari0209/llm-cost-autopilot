from decimal import Decimal

from app.services.cost import calculate_cost


def test_cost_basic():
    # 1M input at $1 + 1M output at $2 = $3
    assert calculate_cost(1_000_000, 1_000_000, Decimal("1"), Decimal("2")) == Decimal("3")


def test_cost_small():
    # 1000 input at $0.10/1M = 0.0001
    assert calculate_cost(1000, 0, Decimal("0.10"), Decimal("0")) == Decimal("0.0001")