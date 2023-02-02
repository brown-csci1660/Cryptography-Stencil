#!/usr/bin/python3

from sys import argv
from subprocess import Popen, PIPE

if len(argv) != 2:
    print("Usage: ./sol.py <path-to-string>\n")
    exit(1)

path = argv[1]

# call this on your answer

def print_answer(A, B, C, D, Anum, Cnum, Nnum):

	print("A cipher hex:", A.hex())
	print("B cipher hex:", B.hex())
	print("C cipher hex:", C.hex())
	print("N cipher hex:", N.hex())
	print("As: %d\nCs: %d\nNs: %d\n" % (Anum, Cnum, Nnum))

