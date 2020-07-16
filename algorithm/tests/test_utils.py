import pytest
from hypothesis import given
from hypothesis.strategies import integers
from rsa import decode_key
from rsa import encode_key
from rsa import powmod


@given(integers(min_value=2), integers(max_value=-1), integers(min_value=2))
def test_powmod_no_multiplicative_inverse(n, e, m):
    with pytest.raises(ValueError):
        powmod(n, e, m * n)


def test_encode_key_overflow():
    assert encode_key(200, 130) == "yA==.ggA="


@pytest.mark.parametrize(
    "key", ["A valid key contains exactly 1 dot", "This.one.has.too.many"]
)
def test_invalid_number_of_dots_in_decode_key_raises_exception(key):
    with pytest.raises(ValueError):
        decode_key(key)
