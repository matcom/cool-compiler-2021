
FILE="./main.py"
INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "COOL Compiler v1.0.0"
echo "Copyright (c) 2021: Juan José López, Juan Carlos Esquivel, Ariel Plasencia"

# echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
python $FILE $INPUT_FILE $OUTPUT_FILE
