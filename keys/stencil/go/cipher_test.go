package main

import (
	"encoding/binary"
	"math/rand"
	"testing"
)

// TestSanity tests to make sure that
// the encryption and decryption work
// (in particular, that decryption under
// a key, k, is the inverse of encryption
// under k)
func TestSanity(t *testing.T) {
	rand.Seed(106641924)
	for i := 0; i < 100; i++ {
		k := rand.Uint32()
		for j := 0; j < 100; j++ {
			var m [8]byte
			binary.BigEndian.PutUint32(m[:], rand.Uint32())
			binary.BigEndian.PutUint32(m[4:], rand.Uint32())
			c := Encrypt(k, m)
			mm := Decrypt(k, c)
			if mm != m {
				t.Errorf("D(k, E(k, m)) != m for k:%v, m:%v, c:%v, m':%v", k, m, c, mm)
			}
		}
	}
}

// TestSanityDouble tests to make sure that
// double encryption and double decryption
// work (in particular, that double decryption
// under a key, (k1, k2), is the inverse of
// double encryption under (k1, k2))
func TestSanityDouble(t *testing.T) {
	rand.Seed(610512501)
	for i := 0; i < 100; i++ {
		k1 := rand.Uint32()
		k2 := rand.Uint32()
		for j := 0; j < 100; j++ {
			var m [8]byte
			binary.BigEndian.PutUint32(m[:], rand.Uint32())
			binary.BigEndian.PutUint32(m[4:], rand.Uint32())
			c := DoubleEncrypt(k1, k2, m)
			mm := DoubleDecrypt(k1, k2, c)
			if mm != m {
				t.Errorf("D(k, E(k, m)) != m for k:(%v, %v), m:%v, c:%v, m':%v", k1, k2, m, c, mm)
			}
		}
	}
}

func BenchmarkEncrypt(b *testing.B) {
	rand.Seed(302228821)
	// Generate 1 c and b.N ks to simulate
	// how this will be used by students
	ks := make([]uint32, b.N)
	for i := range ks {
		ks[i] = rand.Uint32()
	}
	var m [8]byte
	binary.BigEndian.PutUint32(m[:], rand.Uint32())
	binary.BigEndian.PutUint32(m[4:], rand.Uint32())
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Encrypt(ks[i], m)
	}
}

func BenchmarkDecrypt(b *testing.B) {
	rand.Seed(302228821)
	// Generate 1 c and b.N ks to simulate
	// how this will be used by students
	ks := make([]uint32, b.N)
	for i := range ks {
		ks[i] = rand.Uint32()
	}
	var c [8]byte
	binary.BigEndian.PutUint32(c[:], rand.Uint32())
	binary.BigEndian.PutUint32(c[4:], rand.Uint32())
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Decrypt(ks[i], c)
	}
}

func BenchmarkDoubleEncrypt(b *testing.B) {
	rand.Seed(302228821)
	// Generate 1 c and b.N ks to simulate
	// how this will be used by students
	k1s := make([]uint32, b.N)
	k2s := make([]uint32, b.N)
	for i := range k1s {
		k1s[i] = rand.Uint32()
		k2s[i] = rand.Uint32()
	}
	var m [8]byte
	binary.BigEndian.PutUint32(m[:], rand.Uint32())
	binary.BigEndian.PutUint32(m[4:], rand.Uint32())
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		DoubleEncrypt(k1s[i], k2s[i], m)
	}
}

func BenchmarkDoubleDecrypt(b *testing.B) {
	rand.Seed(302228821)
	// Generate 1 c and b.N ks to simulate
	// how this will be used by students
	k1s := make([]uint32, b.N)
	k2s := make([]uint32, b.N)
	for i := range k1s {
		k1s[i] = rand.Uint32()
		k2s[i] = rand.Uint32()
	}
	var c [8]byte
	binary.BigEndian.PutUint32(c[:], rand.Uint32())
	binary.BigEndian.PutUint32(c[4:], rand.Uint32())
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		DoubleDecrypt(k1s[i], k2s[i], c)
	}
}
