import pytest

from numerorum_primorum.utils import (
    ctz,
    has_int_quadratic_root,
    ilog2,
    is_cullen_number,
    is_even,
    is_fermat_number,
    is_fibonacci_number,
    is_mersenne_number,
    is_n_2_pow_n,
    is_negative,
    is_odd,
    is_positive,
    is_pow2,
    is_square,
    is_woodall_number,
)


@pytest.mark.parametrize(
    "a, b, c, T, expected",
    [
        (0, 1, 1, 0, False),
        (1, 0, 1, 0, False),
        (1, 1, -1, 0, False),
        (4, 0, -1, 0, False),
        (1, -3, 2, 0, True),
        (1, 2, 1, 0, True),
        (1, 0, -4, 0, True),
        (2, 3, 1, 0, True),
    ],
)
def test_has_int_quadratic_root(a, b, c, T, expected):
    assert has_int_quadratic_root(a, b, c, T) == expected


@pytest.mark.parametrize(
    "x, expected", [(-1, False), (0, True), (1, True), (2, True), (3, True), (4, False)]
)
def test_is_fibonacci_number(x, expected):
    assert is_fibonacci_number(x) == expected


@pytest.mark.parametrize(
    "x, expected", [(-1, False), (0, False), (1, True), (2, False), (7, True)]
)
def test_is_woodall_number(x, expected):
    assert is_woodall_number(x) == expected


@pytest.mark.parametrize(
    "x, expected", [(-1, False), (0, False), (1, True), (2, False), (3, True)]
)
def test_is_cullen_number(x, expected):
    assert is_cullen_number(x) == expected


@pytest.mark.parametrize(
    "x, expected", [(-1, False), (0, False), (1, False), (2, False), (3, True)]
)
def test_is_fermat_number(x, expected):
    assert is_fermat_number(x) == expected


@pytest.mark.parametrize("x, expected", [(-1, False), (0, True), (1, True), (2, False)])
def test_is_mersenne_number(x, expected):
    assert is_mersenne_number(x) == expected


@pytest.mark.parametrize(
    "x, expected", [(-1, False), (0, False), (1, False), (2, True)]
)
def test_is_n_2_pow_n(x, expected):
    assert is_n_2_pow_n(x) == expected


@pytest.mark.parametrize("x, expected", [(-1, False), (0, True), (1, True), (2, False)])
def test_is_square(x, expected):
    assert is_square(x) == expected


@pytest.mark.parametrize("x, expected", [(-2, 1), (-1, 0), (1, 0), (2, 1)])
def test_ctz(x, expected):
    assert ctz(x) == expected


def test_ctz_0():
    with pytest.raises(ValueError):
        ctz(0)


@pytest.mark.parametrize("x, expected", [(1, 0), (2, 1), (3, 1), (4, 2)])
def test_ilog2(x, expected):
    assert ilog2(x) == expected


def test_ilog2_non_positive():
    with pytest.raises(ValueError):
        ilog2(0)
    with pytest.raises(ValueError):
        ilog2(-1)


@pytest.mark.parametrize(
    "x, expected", [(-1, False), (0, False), (1, True), (2, True), (3, False)]
)
def test_is_pow2(x, expected):
    assert is_pow2(x) == expected


@pytest.mark.parametrize("x, expected", [(-1, False), (0, False), (1, True)])
def test_is_positive(x, expected):
    assert is_positive(x) == expected


@pytest.mark.parametrize("x, expected", [(-1, True), (0, False), (1, False)])
def test_is_negative(x, expected):
    assert is_negative(x) == expected


@pytest.mark.parametrize(
    "x, expected", [(-2, True), (-1, False), (0, True), (1, False), (2, True)]
)
def test_is_even(x, expected):
    assert is_even(x) == expected


@pytest.mark.parametrize(
    "x, expected", [(-2, False), (-1, True), (0, False), (1, True), (2, False)]
)
def test_is_odd(x, expected):
    assert is_odd(x) == expected
