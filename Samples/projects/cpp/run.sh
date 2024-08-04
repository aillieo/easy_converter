#!/bin/bash

SRC_DIR="./src"
INC_DIR="./src"


EXECUTABLE_PATH="./bin"
EXECUTABLE_FILE_NAME="sample"


if [ ! -d "$EXECUTABLE_PATH" ]; then
    mkdir -p "$EXECUTABLE_PATH"
fi


# Find compiler
COMPILER=""
if command -v clang++ &> /dev/null; then
    COMPILER="clang++"
elif command -v g++ &> /dev/null; then
    COMPILER="g++"
elif command -v cl &> /dev/null; then
    COMPILER="cl"
else
    echo "No suitable compiler found. Please install clang++, g++ or MSVC."
    exit 1
fi


FILE_FULL_PATH="$EXECUTABLE_PATH/$EXECUTABLE_FILE_NAME"
if [ "$COMPILER" = "cl" ]; then
    FILE_FULL_PATH="$FILE_FULL_PATH.exe"
fi

echo "Compiler: $COMPILER"

# Compile with the selected compiler
if [ "$COMPILER" = "cl" ]; then
    # MSVC
    cl "$SRC_DIR"/*.cpp /I"$INC_DIR" /Fe"$FILE_FULL_PATH.exe"
else
    # clang++ or g++
    $COMPILER "$SRC_DIR"/*.cpp -I"$INC_DIR" -o "$FILE_FULL_PATH"
fi

# Check if compilation was successful
if [ $? -ne 0 ]; then
    echo "Compilation failed."
    exit 1
else
    echo "Compilation successful."
fi

./$FILE_FULL_PATH
