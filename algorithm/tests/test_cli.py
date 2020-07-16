import random

import pytest
from rsa import cli


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


def test_keygen(capfd, public_key, private_key):
    random.seed(0)
    cli.main(["keygen", "512"])
    captured = capfd.readouterr()
    assert captured.out == f"{public_key}\n{private_key}\n"


def test_encrypt(capsys, message, public_key, ciphertext):
    cli.main(["encrypt", message, public_key])
    captured = capsys.readouterr()
    assert captured.out == f"{ciphertext}\n"


def test_decrypt(capsys, private_key, ciphertext, message):
    cli.main(["decrypt", ciphertext, private_key])
    captured = capsys.readouterr()
    assert captured.out == f"{message}\n"


def test_commands_writing_to_files(
    tmpdir, capsys, public_key, private_key, ciphertext, message
):
    public_key_path = tmpdir / "public_key"
    private_key_path = tmpdir / "private_key"
    ciphertext_path = tmpdir / "ciphertext"
    message_path = tmpdir / "message"

    random.seed(0)
    cli.main(["-o", f"{public_key_path},{private_key_path}", "keygen", "512"])
    assert public_key_path.read_text("utf8") == public_key
    assert private_key_path.read_text("utf8") == private_key

    status = cli.main(["-o", str(public_key_path), "keygen", "512"])
    assert status == 1

    cli.main(["-o", str(ciphertext_path), "encrypt", message, public_key])
    assert ciphertext_path.read_text("utf8") == ciphertext

    cli.main(["-o", str(message_path), "decrypt", ciphertext, private_key])
    assert message_path.read_text("utf8") == message
