.PHONY: clean

main:
	# Compiling the compiler :)

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}

testsum:
	pytest ../tests --tb=no --disable-warnings -m=${TAG}

style:
	for f in **/*.py; do [ -f $$f ] && black $$f && isort --profile black $$f; done
