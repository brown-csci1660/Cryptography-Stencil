package main

import (
	"bufio"
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"os"
	"strings"

	// This module provides the encrypt/decrypt functions
	// used for the cipher in this problem
	"keys/pkg/cipher"
)

type pair struct {
	plaintext  [8]byte
	ciphertext [8]byte
}

func main() {
	if len(os.Args) != 2 {
		fmt.Printf("%v <pairs file>\n", os.Args[0])
		os.Exit(1)
	}

	pairsFile := os.Args[1]

	pairs := parsePairs(pairsFile)
	if len(pairs) == 0 {
		fmt.Fprintf(os.Stderr, "need at least one plaintext/ciphertext pair\n")
		os.Exit(1)
	}

	// TODO: Implement your attack here

	// ******** EXAMPLE CIPHER USAGE (comment or remove this) ******
	// Note:  you have access to the encrypt/decrypt algorithm
	// for the cipher in this problem.
	// Here's an example encryption/decryption:
	somePlaintext := [8]byte{0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07}
	k := uint32(0x00abcdef)
	c := cipher.Encrypt(k, somePlaintext)

	samePlaintext := cipher.Decrypt(k, c)
	if somePlaintext != samePlaintext {
		panic("Something wrong with test example")
	}

	// The library also provides functions to perform the
	// "double encryption":
	// c := cipher.DoubleEncrypt(...)
	// p := cipher.DoubleDecrypt(...)
	// see ./pkg/cipher/cipher.go for details.

	// ******** END EXAMPLE ******

	printKeyPair(0, 0)
}

func printKeyPair(k1, k2 uint32) {
	var k1bytes [4]byte
	var k2bytes [4]byte
	binary.BigEndian.PutUint32(k1bytes[:], k1)
	binary.BigEndian.PutUint32(k2bytes[:], k2)
	fmt.Printf("Recovered key pair: (%v, %v)\n", hex.EncodeToString(k1bytes[1:]), hex.EncodeToString(k2bytes[1:]))
}

// parsePairs reads lines of the form
// <plaintext> <ciphertext>
// from stdin. If it encounters an error,
// it prints the error and exits.
func parsePairs(pairsFile string) []pair {
	var pairs []pair

	fd, err := os.Open(pairsFile)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error opening pairs file: %v\n", err)
		os.Exit(1)
	}
	defer fd.Close()

	s := bufio.NewScanner(fd)
	for s.Scan() {
		parts := strings.Fields(s.Text())
		if len(parts) == 0 {
			// skip empty lines
			continue
		}
		if len(parts) != 2 {
			fmt.Println(os.Stderr, "invalid syntax: expected lines of the form <plaintext> <ciphertext>\n")
			os.Exit(1)
		}
		plainBytes, err := hex.DecodeString(parts[0])
		if err != nil {
			fmt.Fprintf(os.Stderr, "could not parse plaintext as hex: %v\n", err)
			os.Exit(1)
		}
		cipherBytes, err := hex.DecodeString(parts[1])
		if err != nil {
			fmt.Fprintf(os.Stderr, "could not parse plaintext as hex: %v\n", err)
			os.Exit(1)
		}

		if len(plainBytes) != 8 {
			fmt.Fprintf(os.Stderr, "plaintext must be 8 bytes\n", err)
			os.Exit(1)
		}
		if len(cipherBytes) != 8 {
			fmt.Fprintf(os.Stderr, "ciphertext must be 8 bytes\n", err)
		}

		var newPair pair
		copy(newPair.plaintext[:], plainBytes)
		copy(newPair.ciphertext[:], cipherBytes)
		pairs = append(pairs, newPair)
	}
	if err := s.Err(); err != nil {
		fmt.Fprintf(os.Stderr, "could not read stdin: %v\n", err)
		os.Exit(1)
	}
	return pairs
}
