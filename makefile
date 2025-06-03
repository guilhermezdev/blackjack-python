# Variables
PROJECT_NAME = main
SPEC_FILE = main.spec
DIST_DIR = dist
BUILD_DIR = build

# Default target
all: clean build

# Build using the .spec file
build:
	@echo Building the project...
	pyinstaller $(SPEC_FILE)

# Run the built executable
run:
	@echo Running the executable...
	$(DIST_DIR)\$(PROJECT_NAME)\$(PROJECT_NAME).exe

# Clean build artifacts but keep the spec file
clean:
	@echo Cleaning build folders...
	if exist $(BUILD_DIR) rmdir /s /q $(BUILD_DIR)
	if exist $(DIST_DIR) rmdir /s /q $(DIST_DIR)
	if exist __pycache__ rmdir /s /q __pycache__
	del /f /q *.pyc 2>nul

# Clean only compiled Python files
clean-pyc:
	@echo Cleaning .pyc files...
	del /f /q /s *.pyc 2>nul

.PHONY: all build run clean clean-pyc
