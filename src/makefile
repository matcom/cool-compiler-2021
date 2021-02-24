.PHONY: clean

main:
	# Compiling the compiler :)

install:
	pip3 install ply
	pip3 install PyQt5
	pip3 install pytest
	pip3 install pytest-ordering

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}
