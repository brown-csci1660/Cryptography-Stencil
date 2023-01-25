package main

import (
	"fmt"
	"net"
	"os"
	// TODO: Add other imports here if necessary.
)

// An abstraction for sending data to the server.
type PaddingServer struct {
	addr string
	sock net.Conn
}

// NOTE: You do not need to modify this function.
func NewPaddingServer(addr string) (p PaddingServer) {
	p = PaddingServer{addr: addr}
	return p
}

// NOTE: You do not need to modify this function.
func (p *PaddingServer) Connect() {
	// Connect to the server:
	conn, err := net.Dial("tcp", p.addr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "could not connect to server at %s: %v\n", p.addr, err)
		os.Exit(1)
	}
	p.sock = conn
}

// NOTE: You do not need to modify this function.
func (p *PaddingServer) Close() {
	p.sock.Close()
}

func (p *PaddingServer) Send(msg string) {
	// TODO: Use the socket (p.sock) to send the message in the `msg` variable
	// over the wire.
	//
	// Example: fmt.Fprintf(g.sock, "message goes here\n")
}

func (p *PaddingServer) Recv() (msg string) {
	// TODO: Use the socket (p.sock) to read data from the wire. Assign the
	// read data to the `msg` variable.
	//
	// Example: response, err := bufio.NewReader(g.sock).ReadString('\n')

	return msg
}

func sendCommand(addr string, cmd string) {
	p := NewPaddingServer(addr)
	p.Connect()

    // TODO: Implement an attack on the server that takes advantage of the
    // padding leak to send the command in `cmd` to the server using
    // `p.Send` and `p.Recv`.

	p.Close()
}

// NOTE: You do not need to modify this function.
func main() {
	// Check that we have a valid number of arguments:
	if len(os.Args) != 4 {
		fmt.Fprintf(os.Stderr, "Usage: %v <host> <port> <command>\n", os.Args[0])
		os.Exit(1)
	}

	// Parse initial arguments:
	host := os.Args[1]
	port := os.Args[2]
	commandToRun := os.Args[3]

	// Run the guessing game:
	serverAddr := host + ":" + port
	sendCommand(serverAddr, commandToRun)
}
