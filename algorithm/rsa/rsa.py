"""Implementation of core functions of RSA cryptosystem.
"""
import base64
from typing import Tuple
from typing import Union

from . import config
from .primes import find_prime
from .utils import decode_key
from .utils import encode_key
from .utils import lcm
from .utils import powmod
from .utils import xgcd


def initialize(num_bits: int) -> Tuple[int, int, int, int, int, int]:
    """Generate RSA all parameters needed by the RSA algorithm.

    The following parameters are generated:
        - p: a random prime
        - q: a random prime
        - n: product of p and q
        - phi: lcm(p-1, q - 1)
        - e: 65_537
        - d: modular multiplicative inverse of e modulo phi

    Args:
        num_bits: number of bits in primes to be generated

    Returns:
        p, q, n, e, d, phi
    """
    p = find_prime(num_bits)
    q = find_prime(num_bits)
    n = p * q
    phi = lcm(p - 1, q - 1)
    e = 65_537
    _, d, _ = xgcd(e, phi)

    return p, q, n, e, d, phi


def encrypt(string: Union[str, bytes], n: int, e: int) -> bytes:
    """Encrypt message using a key made up of modulus and exponent.

    The string is first converted to bytes which then are converted into a big
    integer :code:`num`. The message is decrypted by calculating
    :code:`num ** e % n`.

    Args:
        string: message to be encrypted
        n: modulus
        e: exponent

    Returns:
        encrypted message
    """
    if isinstance(string, str):
        text = int.from_bytes(string.encode(config.ENCODING), config.BYTEORDER)
    else:
        text = int.from_bytes(string, config.BYTEORDER)
    text = powmod(text, e, n)

    return text.to_bytes((text.bit_length() + 7) // 8, config.BYTEORDER)


def decrypt(string: bytes, n: int, d: int) -> str:
    """Decrypt message using a key made up of modulus and exponent.

    Incoming bytes are converted into a big integer :code:`num`. The message is
    decrypted by calculating :code:`num ** d % n`.

    Args:
        string: encrypted message
        n: modulus
        d: exponent

    Returns:
        decrypted message
    """
    ciphertext = int.from_bytes(string, config.BYTEORDER)
    ciphertext = powmod(ciphertext, d, n)

    return ciphertext.to_bytes(
        (ciphertext.bit_length() + 7) // 8, config.BYTEORDER
    ).decode(config.ENCODING)


def keygen(num_bits: int) -> Tuple[str, str]:
    """Generates pair of base64-encoded keys.

    Args:
        num_bits: number of bits in primes used by the RSA

    Returns:
        base64 encoded public and private key
    """
    *_, n, e, d, _ = initialize(num_bits)
    return encode_key(n, e), encode_key(n, d)


def base64_encrypt(message: str, key: str) -> str:
    """Encrypt and base64-encode message using base64-encoded key.

    Args:
        message: message to be encrypted
        key: base64 encoded key

    Returns:
        base64 encoded ciphertext
    """
    mod, exp = decode_key(key)
    n = (mod.bit_length() + 7) // 8 - 1
    message_bytes = message.encode(config.ENCODING)
    return ".".join(
        base64.urlsafe_b64encode(encrypt(message_bytes[i : i + n], mod, exp)).decode()
        for i in range(0, len(message_bytes), n)
    )


def base64_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt base64-encoded ciphertext using base64-encoded key.

    Args:
        ciphertext: base64 encoded ciphertext
        key: base64 encoded key

    Returns:
        decrypted message
    """
    mod, exp = decode_key(key)
    return "".join(
        decrypt(base64.urlsafe_b64decode(chunk), mod, exp)
        for chunk in ciphertext.split(".")
    )
