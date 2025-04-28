.PHONY: all lint test build package clean

# Run everything
all: lint test build package

# Linting
lint:
	@echo "🔎 Running linter..."
	@./lint.sh

# Testing
test:
	@echo "🧪 Running tests..."
	@./test.sh

# Build (simulate preparing files for release)
build:
	@echo "🏗️ Building project..."
	@rm -rf build
	@mkdir build
	@cp -r src build/
	@cp -r tests build/
	@cp mypl build/
	@echo "Build complete ✅"

# Package (zip everything inside build/)
package:
	@echo "📦 Packaging project..."
	@cd build && zip -r mypl-release.zip * > /dev/null
	@echo "Packaging complete ✅"

# Cleanup
clean:
	@echo "🧹 Cleaning build and cache files..."
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@rm -rf build
	@echo "Cleanup finished ✅"
