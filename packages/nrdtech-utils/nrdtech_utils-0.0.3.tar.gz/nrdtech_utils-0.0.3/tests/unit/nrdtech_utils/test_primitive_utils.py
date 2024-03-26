from decimal import Decimal

from nrdtech_utils.primitive_utils import try_int, convert_float_to_decimal


# Tests for try_int
def test_try_int_with_integer():
    assert try_int(5) == 5


def test_try_int_with_float():
    assert try_int(3.14) == 3


def test_try_int_with_convertible_string():
    assert try_int("8") == 8


def test_try_int_with_non_convertible_string():
    assert try_int("abc") is None


def test_try_int_with_none():
    assert try_int(None) is None


# Tests for convert_float_to_decimal
def test_convert_float_to_decimal_with_float():
    assert convert_float_to_decimal(3.14) == Decimal("3.14")


def test_convert_float_to_decimal_with_high_precision_float():
    assert convert_float_to_decimal(3.141592653589793238462643383279) == Decimal("3.14")


def test_convert_float_to_decimal_with_zero():
    assert convert_float_to_decimal(0.0) == Decimal("0.00")


def test_convert_float_to_decimal_with_none():
    assert convert_float_to_decimal(None) is None


def test_convert_float_to_decimal_with_negative_float():
    assert convert_float_to_decimal(-2.718) == Decimal("-2.72")


def test_convert_float_to_decimal_with_large_float():
    assert convert_float_to_decimal(1234567890.123456789) == Decimal("1234567890.12")
