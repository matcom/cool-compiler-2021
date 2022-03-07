INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "COOL-Compiler v0.0.1"
echo "Copyright (c) 2021: Samuel David Suárez Roddríguez, Enmanuel Verdesia Suárez"

# echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

python3 coolc.py $INPUT_FILE
