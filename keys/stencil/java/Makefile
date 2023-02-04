JAVA := java
JAVAC := javac

OUT_DIR := out

SOURCES=$(shell find . -name '*.java')

all: build

build: $(SOURCES)
	mkdir -pv $(OUT_DIR)
	$(JAVAC) -cp . -d $(OUT_DIR) $(SOURCES)

clean:
	rm -rfv $(OUT_DIR)
