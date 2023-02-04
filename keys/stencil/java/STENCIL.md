## Java stencil

This folder contains Java stencil code for the Cryptography
project.  To use it, please copy the contents of this folder to the
main directory for this problem (ie, `grades`, `ivy`, `keys`, etc.).  

All source files for this stencil can be found in the `src`
directory.  Additionally, we have provided a `Makefile` and run script
(`sol`) to assist with compiling and running your code, which are
described below.  

## Compiling your code

Most users develop for Java in an IDE, which compiles your code
automaticall.  However, we also need to build your code in our
autograder, which means we need a standard way to compile your code
outside of any IDE.   

A `Makefile` has been provided to handle this task.  Even if you
develop your code in an IDE, you **MUST** make sure your code compiles
using the `Makefile` to ensure it runs in our autograder.  

To build your code, run:
```
make
```

**Note**: If you change the layout of your source files, you will also
need to adjust the Makefile.  (This should not be necessary to
complete the project.)

## Running your code

We have provided a run script to that can run your code in a way that
is compatible with our autograder.  Even if you develop your code in
an IDE, you **MUST** make sure your code compiles
using the `Makefile` to ensure it runs in our autograder.  

To run your code using the run script:

1. Run `make` to compile your code (even if it already builds in your
   IDE!)
   
2. Run the run script as follows:
```
./sol <pairs file>
```

where `<pairs file>` is the key pair file required for this problem.
For more information on what this means, see the assignment document.  

**Note**: If you change the layout of your source files or location of
the `main` function, you will also need to modify the run script.  (This
should not be necessary to complete the project.)

## Stencil code overview

You can use any functions in the provided stencil code:
 - Cipher.java contains functions for performing encryption/decryption
   using the crypto scheme in the assignment.  You can call these
   functions with `Cipher.encrypt(...)`, `Cipher.decrypt(...)`, etc.
 - Main.java reads the "pairs file" generated at the start of the
   assignment, which contains plaintext/ciphertext pairs.  Each pair
   is comprised of `ByteArrayWrapper` objects, which make it easy to
   compare pairs using the standard Java methods (`equals()` and
   `hashCode()`).  
 - `ByteArrayWrapper` (ByteArrayWrapper.java) is a utility class that
 is used to represent plaintexts and ciphertexts in a way that makes
 them easy to compare using the standard Java methods `equals()` and
 `hashCode()`.  Specifically:  
     - `equals()` takes in a `ByteArrayWrapper` and compares it with
     the calling `ByteArrayWrapper`, returning true if both
     `ByteArrayWrapper` objects have the same value. 
     - `hashCode()` deterministically generates an integer from the byte
      array. This can be a useful way to identify a given byte array,
      or use Java data structures like `HashSet` or `HashMap`.  
   
**WARNING**: Do not `==` to compare byte arrays (`byte[]`).  This
checks if the addresses of the arrays are the same, not their
contents.  Instead, all byte arrays should use the `ByteArrayWrapper`
class as described above, which provides an `equals()` method you can
use to compare byte arrays based on their contents.  

