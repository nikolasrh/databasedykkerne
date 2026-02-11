#!/bin/bash
# Last ned eksempel-PDFer fra example-pdfs.csv

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CSV_FILE="$SCRIPT_DIR/example-pdfs.csv"
OUTPUT_DIR="$SCRIPT_DIR/input"

mkdir -p "$OUTPUT_DIR"

# Skip header, read name and url
tail -n +2 "$CSV_FILE" | while IFS=, read -r name url; do
    filename="$OUTPUT_DIR/$name.pdf"
    
    if [ -f "$filename" ]; then
        echo "Filen finnes fra før: $name.pdf"
        continue
    fi
    
    echo "Laster ned: $name.pdf"
    curl -sL -o "$filename" "$url"
done
