
test: test_all.sfc
	f2j -r $< -m stack --inline

test_all.sfc: test_all.sf
	python include.py $< -o $@

.PHONY:
clean:
	rm -f *.java *.class *.sfc
