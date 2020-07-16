from hypothesis import assume
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import text
from rsa import base64_decrypt
from rsa import base64_encrypt
from rsa import config
from rsa import decrypt
from rsa import encrypt
from rsa import initialize
from rsa import keygen

NUM_BITS = 512
NUM_BYTES = NUM_BITS // 4


@given(text(min_size=1, max_size=NUM_BYTES))
@settings(deadline=None)
def test_rsa(message):
    assume(len(message.encode(config.ENCODING)) < NUM_BYTES)
    *_, n, e, d, _ = initialize(NUM_BITS)
    assert decrypt(encrypt(message, n, e), n, d) == message


def test_rsa_base64():
    public, private = keygen(1024)
    message = "Hello world"
    assert base64_decrypt(base64_encrypt(message, public), private) == message
