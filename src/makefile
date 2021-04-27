.PHONY: clean

NAME 	   	:= COOL Compiler
VERSION		:= 2.0.0
DEVELOPERS	:= Juan José López, Juan Carlos Esquivel, Ariel Plasencia
COPYRIGHT  	:= Copyright © 2021: $(DEVELOPERS)

main: ## Compiling the compiler :)
	@echo "Compiling the compiler :)"

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

test: ## Run test cases for each stage
	pytest ../tests -v --tb=short -m=${TAG}

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
