.PHONY: main
main:
	# Compiling the compiler :)

.PHONY: clean
clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

.PHONY: test
test:
	pytest ../tests -v --tb=short -m=${TAG}

.PHONY: lexer parser semantic codegen
lexer parser semantic codegen:
	pytest ../tests --tb=no --disable-warnings -m=$@

.PHONY: test-done
test-done: lexer parser semantic

.PHONY: style
style:
	for f in **/*.py; do [ -f $$f ] && black $$f && isort --profile black $$f; done
