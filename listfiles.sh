#!/bin/bash

# This script lists all the names of files in a specified folder

# Check if a folder path is provided as an argument
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/folder"
  exit 1
fi

# Get the folder path from the script arguments
FOLDER_PATH="$1"

# Check if the specified path is a valid directory
if [ ! -d "$FOLDER_PATH" ]; then
  echo "Error: The specified path is not a valid directory."
  exit 1
fi

# List all the names of files in the specified folder
echo "Listing all files in $FOLDER_PATH:"
ls -l "$FOLDER_PATH" | grep '^-' | awk '{print $9}'
