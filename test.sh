#!/bin/bash
# Run pytest suite silently, verify installation, and show ✅
echo "Running pytest suite..."
echo "Checking if pytest is installed..."
# Check if pytest is installed
if ! command -v pytest &> /dev/null
then
    echo "❌ pytest is not installed."
    echo "Attempting to install pytest silently..."
    pip install pytest > /dev/null 2>&1
    if ! command -v pytest &> /dev/null
    then
        echo "❌ pytest installation failed. Please install manually."
        exit 1
    else
        echo "pytest successfully installed ✅"
    fi
fi

# Run pytest
echo "Running pytest..."
export PYTHONPATH=.
pytest tests/ > /dev/null 2>&1
echo "pytest finished ✅"
