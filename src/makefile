.PHONY: clean

main:
	# Compiling the compiler :)

sample:
	python compiler/__main__.py

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}

poetest:
	poetry run make test
