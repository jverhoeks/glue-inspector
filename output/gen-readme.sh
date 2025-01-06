#!/bin/bash

# Header for the output table
echo -e "# Vulnerability Summary\n\n"

echo -e "filename | critical | high | medium | low | information"
echo -e "-------- | -------- | ---- | ------ | --- | ----------"

# Loop through all markdown files in the current directory
for file in *.md; do
    # Initialize counters for severity levels
    critical=0
    high=0
    medium=0
    low=0
    information=0

    # Process each file line by line and count severity levels
    while IFS= read -r line; do
        case "$line" in
            *"CRITICAL"*)   ((critical++)) ;;
            *"HIGH"*)       ((high++)) ;;
            *"MEDIUM"*)     ((medium++)) ;;
            *"LOW"*)        ((low++)) ;;
            *"INFORMATION"*) ((information++)) ;;
        esac
    done < "$file"

    # Output the result for the current file
    echo -e "[$file]($file) | $critical | $high | $medium | $low | $information"
done
