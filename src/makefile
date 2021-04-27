.PHONY: clean

VERSION := 2.0.0

main: ## Compiling the compiler :)
	# Compiling the compiler :)

version: ## Show the project version
	@echo "COOL Compiler $(VERSION)"

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
