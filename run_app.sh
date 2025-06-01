#!/bin/bash

echo "Cricket Scoreboard Analyzer"
echo "=========================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Python not found! Please install Python from python.org"
        echo "On Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "On macOS: brew install python3"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Python found!"
echo

echo "Installing required packages..."
$PYTHON_CMD -m pip install pyyaml

echo
echo "Starting Cricket Scoreboard Analyzer..."
echo
$PYTHON_CMD gui_app.py

if [ $? -ne 0 ]; then
    echo
    echo "Application closed with error. Check the files and try again."
    read -p "Press Enter to continue..."
fi