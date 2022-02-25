.PHONY: clean

main:

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}
 
install:
	pip install ../requeriments.txt



