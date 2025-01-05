#!/bin/bash

# Get script directory and save current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CURRENT_DIR="$(pwd)"

# Move to script directory
cd "$SCRIPT_DIR"

# Run converter
pyproject-to-setup

# Return to original directory
cd "$CURRENT_DIR"
