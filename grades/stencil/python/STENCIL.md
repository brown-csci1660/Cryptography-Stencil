# Python stencil

This folder contains python stencil code for the Cryptography
project.  To use it, please copy the contents of this folder to the
main directory for this problem (ie, `grades`, `ivy`, etc.).  

To run your code in the autograder, you just need to make sure that
your script is executable and has the name `sol` and is located in the
problem's main directory.  

In other words, it should be possible to run your program with:
```
./sol ...
```

The stencil file should already be set up to conform to these
requirements.  If you run into any issues, please let us know.


## "Do I need a Makefile?"

You should not to add a Makefile unless your code imports Python
packages not installed by default.  If you need to do this, you should
include a Makefile with a `build` target to install any required
packages, like this:

```
all: build

build:
	pip install some-package
	pip install some-other-package
```

Note, however, that this project should not require any non-standard
Python packages.  If you need to add extra libraries, please check
with us first!  
