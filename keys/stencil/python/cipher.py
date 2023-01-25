#!/bin/python3

"""
Implementation of the cipher suite used in the "Keys" problem of CS166's HW1
By Justin Bisignano, Spring 2016
"""

import struct

# Constants used for this problem
ROUNDS = 64
DELTA = 0x9E3779B9

def _validate_input(key, message):
	"""Validates encryption and decryption input.
	Verifies that the key is 24 bit and that the message is 8 bytes."""
	if len(message) != 8:
		raise ValueError("message must be 8 bytes long")
	if key != (key & ((1 << 24) - 1)):
		raise ValueError("key must not be more than 24 bits")


def encrypt(key, message):
	"""Encrypts an 8 byte message with the given key.

	Args:
		key: a 24 bit integer to use as the encryption key.
		message: a byte string of length 8 representing the hex encoded message to encrypt.

	Returns:
		a byte string of length 8 representing the hex encoded ciphertext."""

	_validate_input(key, message)

	ret = bytearray()

	v0 = struct.unpack(">I", bytes(message[0:4]))[0]
	v1 = struct.unpack(">I", bytes(message[4:8]))[0]

	sum_ = 0

	k = [key, key, key, key]

	for _ in range(ROUNDS):
		v0 = (v0 + (((v1<<4 ^ v1>>5) + v1) ^ (sum_ + k[sum_ & 3]))) & 0xFFFFFFFF
		sum_ = (sum_ + DELTA) & 0xFFFFFFFF
		v1 = (v1 + (((v0<<4 ^ v0>>5) + v0) ^ (sum_ + k[sum_>>11 & 3]))) & 0xFFFFFFFF

	ret += struct.pack(">I", v0) + struct.pack(">I", v1)

	return str(ret)


def decrypt(key, ciphertext):
	"""Decrypts an 8 byte message using the given key.

	Args:
		key: a 24 bit integer to use as the decryption key
		ciphertext: a byte string of length 8 representing the hex encoded ciphertext to decrypt.

	Returns:
		a byte string of length 8 representing the hex encoded plaintext message."""

	_validate_input(key, ciphertext)

	ret = bytearray()

	v0 = struct.unpack(">I", bytes(ciphertext[0:4]))[0]
	v1 = struct.unpack(">I", bytes(ciphertext[4:8]))[0]

	sum_ = (DELTA * ROUNDS) & 0xFFFFFFFF

	k = [key, key, key, key]

	for _ in range(ROUNDS):
		v1 = (v1 - (((v0<<4 ^ v0>>5) + v0) ^ (sum_ + k[sum_>>11 & 3]))) & 0xFFFFFFFF
		sum_ = (sum_ - DELTA) & 0xFFFFFFFF
		v0 = (v0 - (((v1<<4 ^ v1>>5) + v1) ^ (sum_ + k[sum_ & 3]))) & 0xFFFFFFFF

	ret += struct.pack(">I", v0) + struct.pack(">I", v1)

	return str(ret)


def double_encrypt(key1, key2, message):
	"""Encrypts a message with key1 and then with key2.
	See encrypt for argument details."""
	return encrypt(key2, encrypt(key1, message))


def double_decrypt(key1, key2, ciphertext):
	"""Decrypts a message with key2 and then with key1.
	See decrypt for argument details."""
	return decrypt(key1, decrypt(key2, ciphertext))
