.PHONY: clean

main:
	@echo ${TAG}

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest-3 ../tests -v --tb=short -m=${TAG} #-p no:warnings
	

