from decimal import Decimal


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    input_price_per_1m: Decimal,
    output_price_per_1m: Decimal,
) -> Decimal:
    return (
        Decimal(input_tokens) * Decimal(input_price_per_1m)
        + Decimal(output_tokens) * Decimal(output_price_per_1m)
    ) / Decimal(1_000_000)