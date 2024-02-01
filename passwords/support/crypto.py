# crypto.py
#
# Tiny library of cryptographic functions for working with password
# databases.
#
# DO NOT MODIFY THIS FILE--it will be replaced by the autograder.
#
import os
import hashlib


def hash(data: bytes) -> bytes:
    """
    Get the SHA1 hash of an input

    Input:  any byte array
    Output:  a byte array containing the hash
    """
    m = hashlib.sha1(data)
    m.update(data)
    return m.digest()


def random_bytes(num_bytes: int) -> bytes:
    """
    Return a byte array of num_bytes bytes
    """

    return os.urandom(num_bytes)
