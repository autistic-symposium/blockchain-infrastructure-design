# -*- encoding: utf-8 -*-
# utils/arithmetics.py
# This class implements math methods used by the other classes.


from decimal import Decimal, getcontext
from src.utils.os_utils import log_error


def div(dividend, divisor) -> Decimal:
    """Return higher precision division."""

    if divisor == 0:
        log_error('Found a zero division error. Returning 0.')
        return 0
    return to_decimal(dividend) / to_decimal(divisor)


def to_decimal(value, precision=None) -> Decimal:
    """Return Decimal value for higher (defined) precision."""

    precision = precision or 22
    getcontext().prec = precision
    return Decimal(value)


def wei_to_eth(num) -> float:
    """Convert wei to eth."""
    
    return num / float(1000000000000000000)


def convert_hex_to_int(hex_string: str) -> int:
    """Convert a hex string to an integer"""

    return int(hex_string, 16)
