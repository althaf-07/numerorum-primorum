from itertools import accumulate, islice, product, repeat
from math import gcd, isqrt, prod
from operator import mul

import sympy as sp
from numpy.polynomial import Polynomial

from numerorum_primorum.utils import (
    has_int_polynomial_root,
    has_int_quadratic_root,
    is_cullen_number,
    is_even,
    is_fermat_number,
    is_fibonacci_number,
    is_mersenne_number,
    is_negative,
    is_odd,
    is_positive,
    is_woodall_number,
)

HEEGNER_NUMS = {1, 2, 3, 7, 11, 19, 43, 67, 163}


# Disclaimer: This algorithm is for educational purposes only. I hope no one will ever
# use this algorithm with bad intentions (as far as I know, there are really no good
# intentions for using this algorithm). If someone does any harm with this algorithm,
# I will not be responsible.
def get_rsa_private_key(N: int, e: int = 65537) -> int:
    if not is_positive(N):
        raise ValueError("N must be a positive integer.")
    if is_even(N):
        raise ValueError("N must be odd.")

    factors = factor_int(N)
    if len(factors) != 2:
        raise ValueError("N must be a semiprime.")

    (p, exp_p), (q, exp_q) = factors.items()
    if exp_p != 1 or exp_q != 1:
        raise ValueError("N must be square-free.")

    phi_N = (p - 1) * (q - 1)
    if not is_coprime(e, phi_N):
        raise ValueError("e must be coprime with Euler's totient of N.")

    return pow(e, -1, phi_N)


def mobius(x: int) -> int:
    if not is_positive(x):
        raise ValueError("x must be a positive integer.")
    if x == 1:
        return 1
    factors = factor_int(x)
    exponents = factors.values()
    if any(e > 1 for e in exponents):
        return 0
    return -1 if is_odd(len(factors)) else 1


def is_square_free(x: int) -> bool:
    return is_positive(x) and all(e == 1 for e in factor_int(x).values())


def is_abundant_number(x: int) -> bool:
    return is_positive(x) and sum_divisors(x) - x > x


def is_perfect_number(x: int) -> bool:
    if not is_positive(x):
        return False
    if is_even(x):
        D = (x << 3) + 1
        isqrt_D = isqrt(D)
        return (isqrt_D * isqrt_D == D) and is_mersenne_prime(isqrt_D >> 1)
    return sum_divisors(x) - x == x


def is_deficient_number(x: int) -> bool:
    return is_positive(x) and sum_divisors(x) - x < x


def is_polynomial_prime(coeffs: list[int], T: int) -> bool:
    len_coeffs = len(coeffs)
    if len_coeffs == 0:
        return False

    # Trim trailing zeros from coeffs
    for i in range(len_coeffs - 1, -1, -1):
        if coeffs[i] != 0:
            len_coeffs -= i - 1
            coeffs = coeffs[: i + 1]
            break
    else:
        return False

    if len_coeffs == 1:
        return coeffs[0] == T and is_prime(T)
    if len_coeffs == 2:
        return (T - coeffs[0]) % coeffs[1] == 0 and is_prime(T)
    if len_coeffs == 3:
        c, b, a = coeffs
        return has_int_quadratic_root(a, b, c, T) and is_prime(T)
    p = Polynomial(coeffs)
    return has_int_polynomial_root(p, coeffs[0], T) and is_prime(T)


def get_divisors(
    x: int, sort: bool = True, include_negative: bool = False
) -> list[int]:
    if x == 0:
        raise ValueError("x must be a non-zero integer.")
    divisors = [1]

    for p, e in factor_int(abs(x)).items():
        powers = list(accumulate(repeat(p, e), mul))
        new_divisors = powers + [prod(pair) for pair in product(powers, divisors[1:])]
        divisors.extend(new_divisors)

    if include_negative:
        divisors.extend([-d for d in divisors])
    return sorted(divisors) if sort else divisors


def sum_divisors(x: int) -> int:
    return prod((p ** (e + 1) - 1) // (p - 1) for p, e in factor_int(x).items())


def count_divisors(x: int) -> int:
    return prod(e + 1 for e in factor_int(x).values())


def get_prime_divisors(x: int) -> list[int]:
    return list(factor_int(abs(x)))


def is_prime_power(x: int) -> bool:
    return is_positive(x) and len(list(islice(factor_int(x), 2))) == 1


def is_heegner_number(x: int) -> bool:
    return x in HEEGNER_NUMS


def is_fibonacci_prime_index(x: int) -> bool:
    return (is_prime(x) and is_prime(int(sp.fibonacci(x)))) or (x == 4)


def is_fibonacci_prime(x: int) -> bool:
    return is_fibonacci_number(x) and is_prime(x)


def is_woodall_prime_index(x: int) -> bool:
    return is_positive(x) and is_prime(x * (1 << x) - 1)


def is_woodall_prime(x: int) -> bool:
    return is_woodall_number(x) and is_prime(x)


def is_cullen_prime_index(x: int) -> bool:
    return not is_negative(x) and is_prime(x * (1 << x) + 1)


def is_cullen_prime(x: int) -> bool:
    return is_cullen_number(x) and is_prime(x)


def is_fermat_prime_index(x: int) -> bool:
    return not is_negative(x) and is_prime((1 << (1 << x)) + 1)


def is_fermat_prime(x: int) -> bool:
    return is_fermat_number(x) and is_prime(x)


def is_mersenne_prime_index(x: int) -> bool:
    return is_prime(x) and is_prime((1 << x) - 1)


def is_mersenne_prime(x: int) -> bool:
    return is_mersenne_number(x) and is_prime(x)


def is_safe_prime(x: int) -> bool:
    return is_prime(x >> 1) and is_prime(x)


def is_sophie_germain_prime(x: int) -> bool:
    return is_prime(x) and is_prime((x << 1) + 1)


def is_sexy_prime(x: int) -> bool:
    return is_prime_pair(x, 6)


def is_cousin_prime(x: int) -> bool:
    return is_prime_pair(x, 4)


def is_twin_prime(x: int) -> bool:
    return is_prime_pair(x, 2)


def is_prime_pair(x: int, gap: int) -> bool:
    if not (is_positive(gap) and is_prime(x)):
        return False
    if is_odd(gap):
        return is_prime(2 + gap) if x == 2 else x - gap == 2
    return is_prime(x - gap) or is_prime(x + gap)


def is_composite(x: int) -> bool:
    return x > 1 and not is_prime(x)


def is_prime(x: int) -> bool:
    return sp.isprime(x)


def factor_int(N: int) -> dict[int, int]:
    return sp.factorint(N)


def is_coprime(*integers: int) -> bool:
    return gcd(*integers) == 1


def main() -> None:
    pass


if __name__ == "__main__":
    main()
