"""Package implementing `RSA cryptosystem <https://en.wikipedia.org/wiki/RSA_(cryptosystem)>`__.

The package implements basic key generation, encryption and decryption. It also
exposes some utility functions needed to perform the main functionalities
(e.g implementations of Rabin-Miller primality test and extended Euclidean
algorithm)

Example:
    >>> from rsa import decrypt, encrypt, initialize
    >>> message = "Hello world!"
    >>> *_, n, e, d, _ = initialize(512)
    >>> ciphertext = encrypt(message, n, e)
    >>> print(decrypt(ciphertext, n, d))
    Hello world!

    The above example exposes low-level details of the algorithm, such as primes
    generated during key generation as well as components of public and private key.
    You can also use higher-level functions which do not deal with integers and
    raw bytes but rather base64 encoded keys and ciphertexts.

    >>> from rsa import keygen, base64_encrypt, base64_decrypt
    >>> message = 'Hello world!'
    >>> public_key, private_key = keygen(512)
    >>> print(base64_decrypt(base64_encrypt(message, public_key), private_key))
    Hello world!

    keygen, base64_encrypt and base64_decrypt are exposed through package cli which is
    documented bellow.
"""
from .primes import find_prime
from .primes import generate_prime_candidate
from .primes import is_prime
from .rsa import base64_decrypt
from .rsa import base64_encrypt
from .rsa import decrypt
from .rsa import encrypt
from .rsa import initialize
from .rsa import keygen
from .utils import decode_key
from .utils import encode_key
from .utils import lcm
from .utils import powmod
from .utils import xgcd

__version__ = "0.1.0"
