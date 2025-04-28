# Makefile for mypl DevOps Final Project

.PHONY: all lint test clean

# Run all steps
all: lint test

# Run linter
lint:
	@echo "🔎 Running linter..."
	@./lint.sh

# Run tests
test:
	@echo "🧪 Running tests..."
	@./test.sh

# Clean pycache files
clean:
	@echo "🧹 Cleaning __pycache__ folders..."
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "Cleanup finished ✅"
