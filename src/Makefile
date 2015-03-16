
include Makefile.inc

.PHONY: all
all: parser

parser: parser.sf
	$(F2J) -c $< $(F2JFLAGS)

test: parser.sf
	$(F2J) -r $< $(F2JFLAGS)

clean:
	rm -f *.java *.class

