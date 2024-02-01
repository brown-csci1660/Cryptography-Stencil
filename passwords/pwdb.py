# pwdb.py
# Helpers for password storage

import support.crypto as crypto

METHOD_PLAIN = "plain"
METHOD_SHA1_NO_SALT = "sha1-nosalt"
METHOD_SHA1_SALT4 = "sha1-salt4"

METHODS = [
    METHOD_PLAIN,
    METHOD_SHA1_NO_SALT,
    METHOD_SHA1_SALT4,
]


