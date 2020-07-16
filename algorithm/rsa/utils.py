"""Utility functions needed for implementing RSA cryptosystem."""
import base64
from math import gcd
from typing import Tuple

from . import config


def lcm(a: int, b: int) -> int:
    """Calculates lowest common multiplier of two integers.

    Args:
        a: first number
        b: second number

    Returns:
        lcm(num1, num2)
    """
    return a * b // gcd(a, b)


def xgcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean algorithm.

    Finds :code:`gcd(a,b)` along with coefficients :code:`x`, :code:`y` such that
    :code:`ax + by = gcd(a,b)`.

    Args:
        a: first number
        b: second number

    Returns:
        gcd(a,b), x, y
    """
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return b, x, y


def powmod(n: int, e: int, m: int) -> int:
    """
    If :code:`e > 0` the implementation falls back to builtin pow. Otherwise finds modular
    multiplicative inverse of :code:`n` (:code:`n^-1`) and calculates :code:`pow(n^-1, -e, m).`
    This is necessary because builtin pow for Python < 3.8 doesn't do this if :code:`e < 0`.

    Args:
        n: base
        e: exponent
        m: modulus

    Returns:
        :code:`n ** e % m`
    """
    if e < 0:
        g, x, _ = xgcd(n, m)
        if g != 1:
            raise ValueError("Modular inverse does not exist!")
        return pow(x % m, -e, m)
    return pow(n, e, m)


def encode_key(mod: int, exp: int) -> str:
    """Base64-encodes public/private key.

    Args:
        mod: modulus
        exp: exponent

    Returns:
        base64-encoded key
    """
    mod_base64 = base64.urlsafe_b64encode(
        mod.to_bytes((mod.bit_length() + 7) // 8, config.BYTEORDER)
    ).decode()

    try:
        exp_base64 = base64.urlsafe_b64encode(
            exp.to_bytes((exp.bit_length() + 7) // 8, config.BYTEORDER, signed=True)
        ).decode()
    except OverflowError:
        exp_base64 = base64.urlsafe_b64encode(
            exp.to_bytes((exp.bit_length() + 7) // 8 + 1, config.BYTEORDER, signed=True)
        ).decode()

    return f"{mod_base64}.{exp_base64}"


def decode_key(key: str) -> Tuple[int, int]:
    """Decodes base64-encoded key into modulus and exponent.

    Args:
        key: base64-encoded key

    Returns:
        modulus, exponent pair
    """
    try:
        mod, exp = key.split(".")
    except ValueError:
        raise ValueError(f"`{key}` is not a valid key")

    return (
        int.from_bytes(base64.urlsafe_b64decode(mod), config.BYTEORDER),
        int.from_bytes(base64.urlsafe_b64decode(exp), config.BYTEORDER, signed=True),
    )
