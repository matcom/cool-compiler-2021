.PHONY: clean

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips
	
	rm -rf ../.pytest_cache 
	rm -rf ./CIL/__pycache__
	rm -rf ./MIPS/__pycache__
	rm -rf ./Lexer/__pycache__
	rm -rf ./Tools/__pycache__
	rm -rf ./Parser/__pycache__
	rm -rf ./Semantic/__pycache__

test:
	pytest-3 ../tests -v --tb=short -m=${TAG} -p no:warnings

