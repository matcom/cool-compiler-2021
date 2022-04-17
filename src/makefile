.DEFAULT_GOAL := info
.PHONY: clean, info, main, test

CODE := code.cl
FILE_NAME := $(shell echo $(CODE) | cut -d '.' -f 1)
ASM	:= $(FILE_NAME).mips

main:
	@./coolc.sh $(CODE)
	@spim -file $(ASM)

clean:
	@rm -rf build/*
	@rm -rf ../tests/*/*.mips

test:
	@pytest ../tests -v --tb=short -m=${TAG}

install:
	@python -m pip install -r ../requirements.txt
	@sudo apt-get install spim

info:
	@echo "Cool Compiler 2021 - CodersUP"