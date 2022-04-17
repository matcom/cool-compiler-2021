.PHONY: clean

main:
	# Compiling the compiler :)

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}

compile:
	python3 coolc.py ../tests/codes/$(s).cl $(p)
