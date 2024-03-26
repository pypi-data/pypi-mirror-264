from decimal import localcontext, Decimal, ROUND_HALF_UP


def try_int(x):
    try:
        return int(x)
    except:
        return None


def convert_float_to_decimal(num: float, precision=2) -> Decimal | None:
    if num is None:
        return None
    with localcontext() as ctx:
        ctx.prec = 28  # Set a higher precision locally
        dec = Decimal(str(num))
        # Dynamically create the quantize pattern based on precision
        quantize_pattern = "0." + "0" * precision if precision > 0 else "0"
        return dec.quantize(Decimal(quantize_pattern), rounding=ROUND_HALF_UP)
