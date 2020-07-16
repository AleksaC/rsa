import json
import random

import pytest
from app import app
from app import json_exceptions


@pytest.fixture
def message():
    return "Hello world"


@pytest.fixture
def public_key():
    return (
        "zXR7l5BTTjoURXPmcc7vtto1GCbi07ygBodsICAzl3O3TG0K9dl1wB1izdy9Ey0Mfur_r_"
        "BFKtb5PeOXY0JVU0dafKw5YT9qndzdvTGKlHKr5xuVAAJx4OQsk1c3A-igZVkm6QEuJlOW"
        "sv0bLKOxjX6X9G9_oh4Kgxm3zudEmJA=.AQAB"
    )


@pytest.fixture
def private_key():
    return (
        "zXR7l5BTTjoURXPmcc7vtto1GCbi07ygBodsICAzl3O3TG0K9dl1wB1izdy9Ey0Mfur_r_"
        "BFKtb5PeOXY0JVU0dafKw5YT9qndzdvTGKlHKr5xuVAAJx4OQsk1c3A-igZVkm6QEuJlOW"
        "sv0bLKOxjX6X9G9_oh4Kgxm3zudEmJA=.MexFXz3esLCNvEBC7tF0X5mors-R46-FZsk4d"
        "PxdW9X4nsXcrtoVGwspSscq4OvIgdKRob033Pcb0XKSH9ui-vdAOuGmWPz-KeZ12rQDlVB"
        "twwdnmXpTwCAj4DEFyOh1o53lVvGEQSm4GUCASHO0mioLv0VhhGFeREAHjrp0dfU="
    )


@pytest.fixture
def ciphertext():
    return (
        "LNOISy6_5SyF3aTlKmJ-NTOD2W-HfkquEvI7zDtVQYsj5exIphiXEhCxEryBl50JUmEn9d"
        "svSqAf-j0JyKg9FiGVyYouNUDvGYRhqBkygmAhZCMRh6NW-7QRtH3f4Biwu_XTvqV43n21"
        "QPgDuovuTPUqG9FvojJy9VFReHKThl8="
    )


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


def test_json_wrapper(client):
    @app.route("/", methods=["GET"])
    @json_exceptions
    def dummy_view_function():
        raise ValueError("Value Error")

    response = client.get("/")
    assert response.status_code == 500
    assert json.loads(response.data) == {"error": "Value Error"}


def test_keygen(client, private_key, public_key):
    random.seed(0)
    response = client.get("/keygen?num_bits=512")
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "private_key": private_key,
        "public_key": public_key,
    }


def test_keygen_with_invalid_parameters(client):
    response = client.get("/keygen?num_bits=1")
    assert response.status_code == 400
    assert json.loads(response.data) == {
        "error": "num_bits should be a positive integer greater or equal to 2"
    }

    response = client.get("/keygen?num_bits=NaN")
    assert response.status_code == 400
    assert json.loads(response.data) == {
        "error": "num_bits should be a positive integer greater or equal to 2"
    }


def test_encrypt(client, public_key, message, ciphertext):
    response = client.get(f"/encrypt?message={message}&key={public_key}")
    assert response.status_code == 200
    assert json.loads(response.data) == {"ciphertext": ciphertext}


def test_encrypt_with_missing_params(client, public_key, message, ciphertext):
    response = client.get(f"/encrypt?key={public_key}")
    assert response.status_code == 400
    assert json.loads(response.data) == {"error": "Message is not provided!\n"}

    response = client.get(f"/encrypt?message={message}")
    assert response.status_code == 400
    assert json.loads(response.data) == {"error": "Encryption key is not provided!\n"}


def test_decrypt(client, private_key, message, ciphertext):
    response = client.get(f"/decrypt?ciphertext={ciphertext}&key={private_key}")
    assert response.status_code == 200
    assert json.loads(response.data) == {"message": message}


def test_decrypt_with_missing_params(client, private_key, message, ciphertext):
    response = client.get(f"/decrypt?key={private_key}")
    assert response.status_code == 400
    assert json.loads(response.data) == {"error": "Ciphertext is not provided!\n"}

    response = client.get(f"/decrypt?ciphertext={ciphertext}")
    assert response.status_code == 400
    assert json.loads(response.data) == {"error": "Decryption key is not provided!\n"}
