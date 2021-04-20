.PHONY: clean

main:
	for file in ../tests/lexer/*.cl; do  ./coolc.sh $$file; done

install:
	pip3 install pytest
	pip3 install pytest-ordering

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}

