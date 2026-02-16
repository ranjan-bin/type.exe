#!/bin/bash
# Helper script to run Terminal Type Racer in the virtual environment

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
if [ -f "$DIR/venv/bin/activate" ]; then
    source "$DIR/venv/bin/activate"
else
    echo "Error: Virtual environment not found in $DIR/venv"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Run the game
python3 "$DIR/main.py" "$@"
