INPUT_FILE=$1
CIL_FILE=${INPUT_FILE:0: -2}cil
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "cool-compiler-2021"
echo "Copyright (c) 2021: Reinaldo Barrera Travieso" 

python3.8 main.py $INPUT_FILE $CIL_FILE $OUTPUT_FILE
