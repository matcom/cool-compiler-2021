.PHONY: clean

main:
	python -m cool_compiler string3.cl

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}

cool_compiler:
	python3.8 -m cool_compiler

codegen:
	python3.8  cool_compiler/codegen/__main__.py

lexer:
	python3.8  cool_compiler/lexer/__main__.py

parser:
	python3.8  cool_compiler/parser/__main__.py

semantic:
	python3.8  cool_compiler/semantic/__main__.py