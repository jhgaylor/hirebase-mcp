.PHONY: install install-dev build clean test all venv

# Default Python command (use python3 explicitly)
PYTHON = python3
# Application name derived from project
APP_NAME = hirebase-mcp
# Source directory
SRC_DIR = src
# Build directory for PyInstaller output
BUILD_DIR = dist
# Virtual environment directory
VENV_DIR = .venv
# UV command
UV = uv

all: venv build

venv:
	$(PYTHON) -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && $(UV) pip install -e .

install: venv
	. $(VENV_DIR)/bin/activate && $(UV) pip install -e .

install-dev: venv
	. $(VENV_DIR)/bin/activate && $(UV) pip install -e ".[dev]"

test: venv
	. $(VENV_DIR)/bin/activate && $(UV) pip install -e ".[test]"
	. $(VENV_DIR)/bin/activate && $(PYTHON) -m pytest

# Build the binary using PyInstaller
build: install-dev
	. $(VENV_DIR)/bin/activate && $(PYTHON) -m PyInstaller --name=$(APP_NAME) --onefile --paths=$(SRC_DIR) --add-data="$(SRC_DIR):src" $(SRC_DIR)/__init__.py

# Clean build artifacts
clean:
	rm -rf build $(BUILD_DIR) __pycache__ *.spec
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Clean everything including virtual environment
clean-all: clean
	rm -rf $(VENV_DIR)

# Help target
help:
	@echo "Available targets:"
	@echo "  all        - Create venv and build binary (default)"
	@echo "  venv       - Create virtual environment and install base dependencies"
	@echo "  install    - Install the package in virtual environment"
	@echo "  install-dev- Install the package with development dependencies (includes PyInstaller)"
	@echo "  test       - Run tests"
	@echo "  build      - Build binary with PyInstaller"
	@echo "  clean      - Remove build artifacts"
	@echo "  clean-all  - Remove build artifacts and virtual environment"
	@echo "  help       - Show this help message" 