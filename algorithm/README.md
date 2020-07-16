# RSA

Python implementation of RSA algorithm.

## Installation
The library has no practical use and for that reason hasn't been published to
PyPI. If for some reason you want to install it, the easiest way to do so is by
running the following command (you can replace master with a sha of a specific
commit):
```shell script
pip install git+https://github.com/AleksaC/rsa.git@master#egg=rsa&subdirectory=algorithm
```

## Example
```python
from rsa import decrypt, encrypt, initialize

message = "Hello world!"
*_, n, e, d, _ = initialize(1024)
ciphertext = encrypt(message, n, e)
print(decrypt(ciphertext, n, d))
```

Check out the [docs](https://rsa-kriptografija.netlify.app) for more examples.
