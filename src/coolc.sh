#!/bin/bash

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "cool-compiler-2021"
echo "Copyright (c) 2021: Reinaldo Barrera Travieso"

python3 main.py $INPUT_FILE $OUTPUT_FILE
