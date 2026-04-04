from math import isqrt

from numpy.polynomial import Polynomial


def has_int_polynomial_root(p: Polynomial, a_0: int, T: int = 0) -> bool:
    from numerorum_primorum.main import get_divisors

    if a_0 == T:
        return True
    divisors = get_divisors(a_0 - T, sort=False, include_negative=True)
    return any(p(d) == T for d in divisors)


def has_int_quadratic_root(a: int, b: int, c: int, T: int = 0) -> bool:
    if a == 0:
        return False
    D = (b * b) - ((a * (c - T)) << 2)
    if is_negative(D):
        return False
    isqrt_D = isqrt(D)
    if isqrt_D * isqrt_D != D:
        return False
    denom = a << 1
    return (-b + isqrt_D) % denom == 0 or (-b - isqrt_D) % denom == 0


def is_fibonacci_number(x: int) -> bool:
    return not is_negative(x) and (is_square(5 * x * x + 4) or is_square(5 * x * x - 4))


# n * 2^n - 1, where n is a positive integer
def is_woodall_number(x: int) -> bool:
    return is_n_2_pow_n(x + 1)


# n * 2^n + 1, where n is a non-negative integer
def is_cullen_number(x: int) -> bool:
    return is_n_2_pow_n(x - 1) or x == 1


# 2^(2^n) + 1, where n is a non-negative integer
def is_fermat_number(x: int) -> bool:
    x -= 1
    return is_pow2(x) and is_pow2(ilog2(x))


# 2^n - 1, where n is a non-negative integer
def is_mersenne_number(x: int) -> bool:
    return is_pow2(x + 1)


# n * 2^n, where n is a positive integer
def is_n_2_pow_n(x: int) -> bool:
    if not is_positive(x):
        return False
    exponent = ctz(x)
    multiple = x >> exponent
    while multiple <= exponent:
        if exponent == multiple:
            return True
        exponent -= 1
        multiple <<= 1
    return False


def is_square(x: int) -> bool:
    if is_negative(x):
        return False
    isqrt_x = isqrt(x)
    return isqrt_x * isqrt_x == x


def ctz(x: int) -> int:
    """Returns the count trailing zeros of x (exponent of factor 2 of x)."""
    if x == 0:
        raise ValueError("x must be a non-zero integer.")
    return ilog2(x & -x)


def ilog2(x: int) -> int:
    """Returns floor(log_2(x))."""
    if not is_positive(x):
        raise ValueError("x must be a positive integer.")
    return x.bit_length() - 1


def is_pow2(x: int) -> bool:
    return is_positive(x) and (x & (x - 1)) == 0


def is_negative(x: int) -> bool:
    return x < 0


def is_positive(x: int) -> bool:
    return x > 0


def is_even(x: int) -> bool:
    return not is_odd(x)


def is_odd(x: int) -> bool:
    return (x & 1) == 1


def main() -> None:
    pass


if __name__ == "__main__":
    main()
