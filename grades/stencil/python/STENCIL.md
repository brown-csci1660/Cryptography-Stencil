# Python stencil

This folder contains python stencil code for the Cryptography
project.  To use it, please copy the contents of this folder to the
main directory for this problem (ie, `grades`, `ivy`, etc.).  

To run your code in the autograder, you just need to make sure that
your script has the name `sol` and is located in the problem's main
directory.  

## "Do I need to change the Makefile?"

You should not need to modify the provided Makefile unless your code
imports Python packages not installed by default.  If you need to do
this, you should update the `build` target of the Makefile to install
any required packages, like this:

```
build:
	pip install some-package
	pip install some-other-package
```

Note, however, that this project should not require any non-standard
Python packages.  If you need to add extra libraries, please check
with us first!  
