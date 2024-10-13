# Makefile for creating a single-file executable for the faceSwapper project using PyInstaller

.PHONY: all clean build

# The entry point of the application
ENTRY_POINT = run.py

# Name of the output executable
EXECUTABLE_NAME = faceSwapper

# Build directory
BUILD_DIR = build
DIST_DIR = dist

all: build

# Build the executable using PyInstaller
build:
	@echo "Building the executable with PyInstaller..."
	pyinstaller --onefile \
		--add-data "config.yaml:." \
		--add-data "faceSwapper-targets/models/inswapper_128_fp16.onnx:faceSwapper-targets/models" \
		--name $(EXECUTABLE_NAME) $(ENTRY_POINT)

# Clean up the build and dist directories
clean:
	@echo "Cleaning up the build and dist directories..."
	rm -rf $(BUILD_DIR) $(DIST_DIR) $(EXECUTABLE_NAME).spec

# Run the application from the dist directory
run:
	@echo "Running the application..."
	./dist/$(EXECUTABLE_NAME)
