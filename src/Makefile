include Makefile.inc

test: test_all.sf
	python include.py $< -o $<c
	${F2J} -r $<c ${F2JFLAGS}

.PHONY: clean
clean:
	sh clean
