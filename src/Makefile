
F2J := f2j
F2J_FLAGS := -m stack

parser: parser.sf
	$(F2J) -c $< $(F2J_FLAGS)

test: parser.sf
	$(F2J) -r $< $(F2J_FLAGS)

clean:
	rm -f *.java *.class

