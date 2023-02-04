#!/usr/bin/python

import sys
import socket
# TODO: Add other imports here if necessary.

class PaddingServer:
    # NOTE: You do not need to modify this function.
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # NOTE: You do not need to modify this function.
    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
        except Exception as e:
            print "[-] Connection failed. ({})".format(e)

    # NOTE: You do not need to modify this function.
    def close(self):
        self.sock.close()

    def send(self, msg):
        # TODO: Use the socket (self.sock) to send the message in the `msg`
        # variable over the wire.
        #
        # Example: self.sock.send("message goes here\n")
        #          This will send "message goes here\n" to the server.
        pass

    def recv(self):
        # TODO: Use the socket (self.sock) to read data from the wire.
        #
        # Example: self.sock.recv(1024)
        #          This reads the first 1024 bytes from the server.
        return ""

def send_command(host, port, cmd):
    p = PaddingServer(host, port)
    p.connect()

    # TODO: Implement an attack on the server that takes advantage of the
    # padding leak to send the command in `cmd` to the server using
    # `p.send` and `p.recv`.

    p.close()

# NOTE: You do not need to modify this function.
def main():
    if len(sys.argv) != 4:
        print "Usage: ./sol.py <host> <port> <command>"
        exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    command_to_run = sys.argv[3]

    send_command(host, port, command_to_run)

# Run the script:
main()
