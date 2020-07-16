"""Prime number checking and generation utilities.

This module contains functions for checking primality and finding big prime numbers.
"""
import random


def is_prime(num: int, num_rounds: int = 40) -> bool:
    """Probabilistically determine if a given number is a prime.

    This function uses `Miller–Rabin <https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test>`__
    primality test to probabilistically determine if the provided number is prime.

    Args:
        num: prime candidate
        num_rounds: number of iterations inside the algorithm

    Returns:
        whether the number is a prime or not
    """
    if num == 2 or num == 3:  # pragma: no cover
        return True
    if num <= 1 or num % 2 == 0:  # pragma: no cover
        return False

    r, d = 0, num - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(num_rounds):
        a = random.randrange(2, num - 1)
        x = pow(a, d, num)

        if x == 1 or x == num - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False

    return True


def generate_prime_candidate(num_bits: int) -> int:
    """Generate a random odd positive integer represented with given number of bits.

    Args:
        num_bits: size of the number in terms of bits required  for representing it

    Returns:
        a random odd natural number of given size
    """
    return random.getrandbits(num_bits) | ((1 << num_bits - 1) | 1)


def find_prime(num_bits: int) -> int:
    """Find a prime represented with given number of bits.

    Generates random numbers of given size until one of them is deemed prime by
    a probabilistic primality check.

    Args:
        num_bits: size of the prime in terms of bits required  for representing it

    Returns:
        a (probably) prime number with given number of bits
    """
    while True:
        num = generate_prime_candidate(num_bits)
        if is_prime(num):
            return num
