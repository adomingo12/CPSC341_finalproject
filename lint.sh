#!/bin/bash
# Run flake8 linter silently, install flake8 quietly if missing, and show ✅

echo "Running flake8 linter..."
echo "Checking if flake8 is installed..."
if ! command -v flake8 &> /dev/null
then
    echo "❌ flake8 is not installed."
    echo "Attempting to install flake8 silently..."
    
    # Install flake8 silently
    pip install flake8 > /dev/null 2>&1

    # After silent install, double-check if it's there
    if ! command -v flake8 &> /dev/null
    then
        echo "❌ flake8 installation failed. Please install manually."
        exit 1
    else
        echo "flake8 successfully installed ✅"
    fi
fi

echo "Running flake8..."
flake8 src/ tests/ > /dev/null 2>&1
echo "flake8 finished ✅"
