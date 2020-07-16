"""REST API exposing rsa package main functionality, namely key generation, encrytion and decryption.
 """
import logging
from functools import wraps

import rsa
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)
logger = logging.getLogger(__file__)


def json_exceptions(func):
    """Wraps view functions to log all uncaught exceptions and return them as a JSON response.

    Args:
        func: view function

    Returns:
        wrapper function
    """

    @wraps(func)
    def wrapper():
        try:
            return func()
        except Exception as e:
            logger.exception(e)
            return jsonify({"error": str(e)}), 500

    return wrapper


@app.route("/keygen", methods=["GET"])
@json_exceptions
def keygen():
    """Generates public/private key pair.

    The endpoint takes a query parameter :code:`num_bits` specifying size in bits of
    prime numbers used in the algorithm. If the parameter is not specified 1024 will
    be used by default.

    Examples:
        .. code::

            $ curl -X GET "http://localhost:5000/keygen?num_bits=512"

    Returns:
        flask.Response with JSON object containing public and private key or error message
    """
    num_bits = request.args.get("num_bits", 1024)

    if isinstance(num_bits, str):  # pragma: no branch
        err_message = "num_bits should be a positive integer greater or equal to 2"
        if not num_bits.isdecimal():
            return jsonify({"error": err_message}), 400
        num_bits = int(num_bits)
        if num_bits < 2:
            return jsonify({"error": err_message}), 400

    public_key, private_key = rsa.keygen(num_bits)

    return jsonify({"public_key": public_key, "private_key": private_key})


@app.route("/encrypt", methods=["GET"])
@json_exceptions
def encrypt():
    """Encrypts the provided message

    The following query parameters need to be provided:
        - :code:`message` - message to be encrypted
        - :code:`key` - key to use for encryption

    Examples:
        .. code::

            $ curl -X GET "http://localhost:5000/encrypt?message=hello&key=5R3MTuM=.AQAB"

    Returns:
        flask.Response with JSON object containing encrypted message or error message
    """
    message = request.args.get("message")
    key = request.args.get("key")

    error = ""

    if message is None:
        error += "Message is not provided!\n"
    if key is None:
        error += "Encryption key is not provided!\n"

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"ciphertext": rsa.base64_encrypt(message, key)})


@app.route("/decrypt", methods=["GET"])
@json_exceptions
def decrypt():
    """Decrypts the provided message

    The following query parameters need to be provided:
        - :code:`ciphertext` - encrypted message to be decrypted
        - :code:`key` - key to use for decryption

    Examples:
        .. code::

            $ curl -X GET "http://localhost:5000/decrypt?ciphertext=Y4q6Xt8=&key=5R3MTuM=.AeymywI="

    Returns:
        flask.Response with JSON object containing decrypted message or error message
    """
    ciphertext = request.args.get("ciphertext")
    key = request.args.get("key")

    error = ""

    if ciphertext is None:
        error += "Ciphertext is not provided!\n"
    if key is None:
        error += "Decryption key is not provided!\n"

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": rsa.base64_decrypt(ciphertext, key)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
