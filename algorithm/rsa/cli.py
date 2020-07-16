"""Package CLI.

This module exposes the package as a command line interface.

Examples:
    .. code::

        $ python -m rsa keygen -o private,public 1024

    The command above writes private and public key to corresponding files.

    .. code::

        $ python -m rsa encrypt -o ciphertext "Hello" $(cat public)

    The command above writes to file a message encrypted using public key generated
    in previous example. The following command decrypts that message using the
    corresponding private key and prints it to the screen.

    .. code::

        $ python -m rsa decrypt $(cat ciphertext) $(cat private)
        Hello

"""
import argparse
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from .rsa import base64_decrypt
from .rsa import base64_encrypt
from .rsa import keygen

ACTIONS: Dict[str, Union[Callable]] = {
    "keygen": keygen,
    "encrypt": base64_encrypt,
    "decrypt": base64_decrypt,
}


def get_parser() -> argparse.ArgumentParser:
    """

    Returns:
        an instance of argument parser
    """
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    keygen_parser = subparsers.add_parser("keygen")
    encrypt_parser = subparsers.add_parser("encrypt")
    decrypt_parser = subparsers.add_parser("decrypt")

    keygen_parser.add_argument("num_bits", type=int)

    encrypt_parser.add_argument("message", type=str)
    encrypt_parser.add_argument("key", type=str)

    decrypt_parser.add_argument("ciphertext", type=str)
    decrypt_parser.add_argument("key", type=str)

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="",
        help="Where to output the results. Defaults to stdout",
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Parses the args and executes the command invoked by them.

    Returns:
        command status code
    """
    parser = get_parser()
    args = vars(parser.parse_args(argv))

    command = args.pop("command")
    action = ACTIONS[command]
    output = args.pop("output")

    res = action(**args)

    if output == "":
        if command == "keygen":
            for key in res:
                print(key)
        else:
            print(res)
    else:
        if command == "keygen":
            dest = output.split(",")
            if len(dest) != 2:
                print(
                    "Please provide a pair of paths to save public and private key to."
                )
                return 1
            for key, file in zip(res, dest):
                with open(file, "w") as f:
                    f.write(key)
        else:
            with open(output, "w") as f:
                f.write(res)

    return 0
