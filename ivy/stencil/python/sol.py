#!/usr/bin/python3

from sys import argv
from subprocess import Popen, PIPE

if len(argv) != 2
    print("Usage: ./sol.py <path to ivy binary to attack>\n")
    exit(1)

ivy_path = argv[1]

ivy_process = Popen(ivy_path, stdin=PIPE, stdout=PIPE, stderr=PIPE)
IVY_STDIN   = ivy_process.stdin
IVY_STDOUT  = ivy_process.stdout
IVY_STDERR  = ivy_process.stderr
