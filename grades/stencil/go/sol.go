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
}
