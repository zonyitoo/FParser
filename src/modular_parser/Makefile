
test: test_all.sf
	python include.py $< -o $<c
	f2j -r $<c -m stack --inline

.PHONY:
clean:
	rm -f *.java *.class *.sfc
