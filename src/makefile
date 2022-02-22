.PHONY: clean

NAME 	   	:= COOL Compiler
VERSION		:= 3.0.0
DEVELOPERS	:= Juan José López, Juan Carlos Esquivel, Carlos Martínez, Ariel Plasencia
COPYRIGHT  	:= Copyright © 2021: $(DEVELOPERS)
UI_FILES	:= about_authors compiler_COOL help orientation

main: ## Compiling the compiler :)
	@echo "Compiling the compiler :)"
	for ui_file in $(UI_FILES); do pyuic5 -x ./uis/$${ui_file}.ui -o ./uis/$${ui_file}.py; done
	python3 utils/remove_character.py

visual: ## Open the app desktop ;)
	python3 visual.py

info: ## Display project description
	@echo "$(NAME) v$(VERSION)"
	@echo "$(COPYRIGHT)"

version: ## Show the project version
	@echo "$(NAME) v$(VERSION)"

install: ## Install the project dependencies
	pip3 install ply
	pip3 install PyQt5
	pip3 install pytest
	pip3 install pytest-ordering

clean: ## Remove temporary files
	rm -rf build/*
	rm -rf ../tests/*/*.mips

my_clean: ## Remove others temporary files
	rm -rf debug/*.*
	rm -rf lexing/__pycache__/
	rm -rf parsing/__pycache__/
	rm -rf parsing/parser.out
	rm -rf parsing/parsetab.py
	rm -rf semantic/__pycache__/
	rm -rf semantic/visitors/__pycache__/
	rm -rf uis/__pycache__/
	rm -rf utils/__pycache__/

test: ## Run test cases for each stage
	pytest ../tests -v --tb=short -m=${TAG}

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
