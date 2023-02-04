package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

const (
	BlockSizeBytes = 8
)

func usage() {
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintf(os.Stderr, "Usage: %v <grades database>\n", os.Args[0])
		os.Exit(1)
	}

	dbPath := os.Args[1]

	fd, err := os.Open(dbPath)
	if err != nil {
		panic(err)
	}
	defer fd.Close()

	reader := bufio.NewReader(fd)
	bytes := make([]byte, BlockSizeBytes)

	for {
		b, err := reader.Read(bytes)
		if err == io.EOF {
			break
		} else if err != nil {
			panic(err)
		}

		// TODO:  process each block

		// TODO: Remove this line (or it will make everything very slow)
		fmt.Printf("Read %d bytes:  %x\n", b, bytes)
	}

	// TODO: Perhaps do some computation, then
	// print out answers for the required questions, using the format
	// specified in the assignment (use the helper function below!)
	//PrintAnswer(...)
}

func PrintAnswer(totalBlocks int, a []byte, b []byte, c []byte, n []byte,
	famousACount int, famousBCount int, famousCCount int, famousNCount int) {
	fmt.Println("Total blocks:", totalBlocks)
	fmt.Printf("Ciphertext for grade A: %x\n", a)
	fmt.Printf("Ciphertext for grade B: %x\n", b)
	fmt.Printf("Ciphertext for grade C: %x\n", c)
	fmt.Printf("Ciphertext for grade N: %x\n", n)
	fmt.Println("Famous student As", famousACount)
	fmt.Println("Famous student Bs", famousBCount)
	fmt.Println("Famous student Cs", famousCCount)
	fmt.Println("Famous student Ns", famousNCount)
}
