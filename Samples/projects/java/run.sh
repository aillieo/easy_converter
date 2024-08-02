#!/bin/bash

# build all the source files in src folder
javac -d ./bin $(find src -name "*.java")

echo ""

# run the main class
java -cp ./bin Main
