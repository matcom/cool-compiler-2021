.PHONY: clean

main:
	@echo "Compiled successfully..."

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips
	rm -rf ../tests/*/*.cil
	
	rm -rf CIL/__pycache__
	rm -rf MIPS/__pycache__
	rm -rf Tools/ 
	rm -rf Parser/__pycache__
	rm -rf Semantic/__pycache__

	rm -rf ../test/__pycache__

	rm -rf ../.pytest_cache
	
test:
	pytest-3 ../tests -v --tb=short -m=${TAG} -p no:warnings
