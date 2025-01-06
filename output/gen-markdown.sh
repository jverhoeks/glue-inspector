#!/bin/bash

# Loop over all requirements-*.txt files
for file in requirements-*.txt; do
    # Extract the version number from the filename
    version=$(echo $file | sed -E 's/requirements-(.*)\.txt/\1/')

    # Set the output markdown file name
    output="${version}.md"

    # Run the trivy command
    trivy fs "$file" \
        --file-patterns "pip:requirements-.*\.txt" \
        --scanners vuln,config,secret,license \
        --list-all-pkgs  \
        --format template \
        --template "@markdown.tpl" \
        --output "$output"

    # Print status message
    echo "Report for $file generated: $output"
done
