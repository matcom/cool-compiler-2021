.PHONY: clean

main:
	for file in ../tests/lexer/*.cl;  do echo $$file; ./coolc.sh $$file; echo; done

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}

