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
// client binary)
func hexStringToBytes(s string) []byte {
	bytes, err := hex.DecodeString(s)
	checkError(err, "Error decoding hex string to bytes")

	return bytes
}

// Validate the test key before running the subprocess
func checkTestKey(key string) {
	b := hexStringToBytes(key)
	if len(b) != 8 {
		panic("Test key must be 8 bytes")
	}
}

func main() {
	// Idea: we can perform our attack automatically by running
	// the client binary as a subprocess--this allows us to
	// repeatedly send commands and read the output as if we were
	// entering input manually, just much faster.
	var ivyProcess *exec.Cmd

	if len(os.Args) == 2 { // Normal operation
		binPath := os.Args[1]
		ivyProcess = exec.Command(binPath) // If test key was specified
	} else if len(os.Args) == 3 {
		binPath := os.Args[1]
		testKey := os.Args[2]
		checkTestKey(testKey)
		ivyProcess = exec.Command(binPath, testKey)
	} else {
		fmt.Printf("%v <path to client binary to attack> [test key]\n", os.Args[0])
		os.Exit(1)
	}

	// Set up a pipe to the client's stdin
	ivyStdin, err := ivyProcess.StdinPipe()
	checkError(err, "Could not open stdin")
	defer ivyStdin.Close()

	// Set up a pipe to the client process' stdout
	ivyStdout, err := ivyProcess.StdoutPipe()
	checkError(err, "Could not open stdout")
	defer ivyStdout.Close()

	// Set up a pipe to the client process' stderr
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
	// the client prints to stdout
	firstResponse, err := reader.ReadString('\n') // Read until newline character
	checkError(err, "Error reading first response")

	firstIv := hexStringToBytes(firstResponse[0:4])
	firstCiphertext := hexStringToBytes(firstResponse[5:21])
	fmt.Printf("First IV:  %x, First c:  %x\n", firstIv, firstCiphertext)

	// TODO: When done, print the recovered key

	// When you have determined the key, print it to stdout as an
	// 8-byte hex string (eg. ababababcdcdcdcd), followed by a
	// newline.  This should be your program's last line of
	// output.  Here's an example:
	// someKey := hexStringToBytes("ababababcdcdcdcd") // Get some byte array
	// fmt.Printf("%x\n", someKey) // Print it as specified
}
