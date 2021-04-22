.PHONY: clean

main:
	./coolc.sh ../tests/lexer/comment1.cl

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}

