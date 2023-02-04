package main

import (
	"bufio"
	"encoding/hex"
	"fmt"
	"os"
	"os/exec"
)

// Helper function to handle checking errors returned by functions. If err is
// not nil, Go aborts by calling panic()
func checkError(err error, msg string) {
	if err != nil {
		panic(err)
	}
}

// Helper to build arrays of bytes from hex strings
// (like those that you type when interacting with the
// router binary)
func hexStringToBytes(s string) []byte {
	bytes, err := hex.DecodeString(s)
	checkError(err, "Error decoding hex string to bytes")

	return bytes
}

func main() {
	if len(os.Args) != 2 {
		fmt.Printf("%v <path to router binary to attack>\n", os.Args[0])
		os.Exit(1)
	}

	// Idea: we can perform our attack automatically by running
	// the router binary as a subprocess--this allows us to
	// repeatedly send commands and read the output as if we were
	// entering input manually, just much faster.

	binPath := os.Args[1]
	ivyProcess := exec.Command(binPath)

	// Set up a pipe to the router's stdin
	ivyStdin, err := ivyProcess.StdinPipe()
	checkError(err, "Could not open stdin")
	defer ivyStdin.Close()

	// Set up a pipe to the router process' stdout
	ivyStdout, err := ivyProcess.StdoutPipe()
	checkError(err, "Could not open stdout")
	defer ivyStdout.Close()

	// Set up a pipe to the router process' stderr
	ivyStderr, err := ivyProcess.StderrPipe()
	checkError(err, "Could not open stderr")
	defer ivyStderr.Close()

	// Create a buffered reader to read from stdout more easily
	reader := bufio.NewReader(ivyStdout)

	// Run the Ivy binary
	err = ivyProcess.Start()
	checkError(err, "Could not run Ivy binary")

	// TODO: Implement your attack here.
	//
	// You can send data to the stdin of the ivy binary with the following:
	//
	//   ivyStdin.Write([]byte("data to send\n"))
	//
	// You can read the next line from the ivy binary's STDOUT with
	// the following:
	//
	//   stdoutReader.ReadString('\n')  // Note: the single quotes are important!
	//                                  // ' denotes single character.
	//                                  // " denotes a string
	//

	// Here's an example of how to use ReadString to get the first line
	// the router prints to stdout
	firstResponse, err := reader.ReadString('\n') // Read until newline character
	checkError(err, "Error reading first response")

	firstIv := hexStringToBytes(firstResponse[0:4])
	firstCiphertext := hexStringToBytes(firstResponse[5:21])
	fmt.Printf("First IV:  %x, First c:  %x\n", firstIv, firstCiphertext)

}
