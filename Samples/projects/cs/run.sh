#!/bin/bash

CURRENT_DIR=$(pwd)
PROJECT_NAME="SampleApp"
PROJECT_FILE="$PROJECT_NAME.csproj"
PROJECT_DIR="$CURRENT_DIR"

if [ ! -f "$PROJECT_FILE" ]; then
    dotnet new console -n "$PROJECT_NAME" -o "$PROJECT_DIR"
    rm "$PROJECT_DIR/Program.cs"
fi

dotnet build "$PROJECT_FILE" -o "$PROJECT_DIR/$PROJECT_NAME/out"

if [ $? -eq 0 ]; then
    dotnet "$PROJECT_DIR/$PROJECT_NAME/out/$PROJECT_NAME.dll"
else
    echo "Compile error."
fi
