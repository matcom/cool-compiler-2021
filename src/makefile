.PHONY: clean

main:
	@./coolc.sh $(CODE)

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}
 
install:
	pip install ../requeriments.txt



