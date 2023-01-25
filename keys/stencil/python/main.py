"""
Main file for the "Keys" problem of CS166's HW1
"""

import sys
import fileinput

from cipher import encrypt, decrypt, double_encrypt, double_decrypt

def main():
	# Pairs is a list of tuples representing plaintext ciphertext 
	# See the read_pairs() docstring for more info
	pairs = read_pairs()

	if len(pairs) == 0:
		print "Error: you must provide at least one plaintext ciphertext pair"
		sys.exit(1)

	#
	# TODO: Implement your attack here
	#
	
	print_keys(0, 0)

	
def print_keys(key1, key2):
	"""Prints a message with the passed integer keys encded in hex."""
	print "Recovered key pair: ({:x}, {:x})".format(key1, key2)


def print_text(message):
	"""Prints the passed plaintext or ciphertext message as a hex encoded string"""
	print message.encode('hex')


def read_pairs():
	"""Reads plaintext ciphertext pairs from stdin.
	Expects the pairs to be of the form "plaintext ciphertext" with each on their own line
	where plaintext and ciphertext are 16 character strings represeing hex encoded numbers
	
	Returns:
		a list of tuples of length 2 containing (plaintext, ciphertext) where
		plaintext and ciphertext are each byte strings of length 8"""

	ret = []

	for line in fileinput.input():
		pair = line.strip().split(" ")

		if len(pair) != 2: error_handler('read invalid line. Expected lines of the form "<plaintext> <ciphertext>"')
		if len(pair[0]) != 16: error_handler('read invalid plaintext length')
		if len(pair[1]) != 16: error_handler('read invalid ciphertext length')

		plaintext = pair[0].decode('hex')
		ciphertext = pair[1].decode('hex')

		if len(plaintext) != 8: error_handler('plaintext must be 8 bytes')
		if len(ciphertext) != 8: error_handler('ciphertext must be 8 bytes')

		ret.append( (plaintext, ciphertext) )

	return ret


def error_handler(message):
	"""Prints an error message and then exits with error code 1"""
	print "Error:", message
	sys.exit(1)


if __name__ == "__main__":
	main()