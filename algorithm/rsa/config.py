"""Package configuration.

This module contains values that need to be consistent accross the entire package.
They were exposed as config so that they may be changed by the user of the package
if there is a need to do so.

Attributes:
    BYTEORDER (str): Can be either 'big' or 'little', signifying that the most
                     significant byte is at the beginning or the end of the array
    ENCODING (str): Which encoding to use when `converting strings to bytes
                    <https://docs.python.org/3/howto/unicode.html#converting-to-bytes>`__


You probably shouldn't change the default values, but if you want to do so you can
see the example bellow to see how. Note that changing config does not update values
imported directly so unless you want them to have the import-time value regardless of
whether config has been changed do not import them directly. For a message to be
decrypted properly the config values need to be the same as those during encryption.

Example:
    `file1.py`

    .. code-block:: python

        >> from rsa import config
        >> config.ENCODING = 'ascii'
        >> import file2
        unicode_escape
        >> import file3
        ascii

    Running the 2 files individually would produce

    `file2.py`

    .. code-block:: python

        >> from rsa import config
        >> print(config.ENCODING)
        unicode_escape

    `file3.py`

    .. code-block:: python

        >> from rsa.config import ENCODING
        >> print(ENCODING)
        unicode_escape
"""

BYTEORDER = "little"
ENCODING = "unicode_escape"
