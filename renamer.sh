#!/bin/bash

# Directory containing the files
dir="/Users/ananthu/Desktop/DOORS/glass/cloud"

# Counter
count=1

# Loop through each file in the directory
for file in "$dir"/*; do
  # Check if it is a file
  if [ -f "$file" ]; then
    # Format the new file name with leading zeros
    new_name=$(printf "V%02d" $count)
    
    # Get file extension
    ext="${file##*.}"
    
    # Rename the file
    mv "$file" "$dir/$new_name.$ext"
    
    # Increment the counter
    ((count++))
  fi
done

echo "Files have been renamed."
