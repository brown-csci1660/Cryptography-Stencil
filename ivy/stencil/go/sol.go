package main

import (
	"fmt"
	"os"
	"os/exec"
)

// Helper function to handle checking errors returned by functions. If err is
// not nil, prints out the given msg to stderr along with a string version of
// err and terminates the program with exit code 1.
func checkError(err error, msg string) {
	if err != nil {
		fmt.Fprintf(os.stderr, "%s: %v\n", msg, err)
		os.Exit(1)
	}
}

func main() {
	// Check that we have a valid number of arguments:
	if len(os.Args) != 2 {
		fmt.Printf("%v <path to ivy binary to attack>\n", os.Args[0])
		os.Exit(1)
	}

	// Prepare to execute the Ivy binary:
	ivyPath    := os.Args[1]
	ivyProcess := exec.Command(ivyPath)

	// Open a stdin pipe to the Ivy binary:
	IVY_STDIN, err := ivyProcess.StdinPipe()
	checkError(err, "Could not open stdin for Ivy binary")
	defer IVY_STDIN.Close()

	// Open a stdout pipe to the Ivy binary:
	IVY_STDOUT, err := ivyProcess.StdoutPipe()
	checkError(err, "Could not open stdout for Ivy binary")
	defer IVY_STDOUT.Close()

	// Open a stderr pipe to the Ivy binary:
	IVY_STDERR, err := ivyProcess.StderrPipe()
	checkError(err, "Could not open stderr for Ivy binary")
	defer IVY_STDERR.Close()

	// Run the Ivy binary:
	err = ivyProcess.Start()
	checkError(err, "Could not run Ivy binary")
	defer ivyProcess.Wait()

	//
	// TODO: Implement your attack here.
	//
	// You can send data to the STDIN of the ivy binary with the following:
	//
	//   IVY_STDIN.puts("data to send")
	//
	// You can read the next line from the ivy binary's STDOUT or STDERR with the
	// following:
	//
	//   IVY_STDOUT.gets
	//
}
