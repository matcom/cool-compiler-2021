INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "Cool Compiler 2021 v1"
echo "Copyright (c): Jose Carlos Hdez, Yan Carlos Glez, Henry Estévez"

FILE="main.py"

python ${FILE} $INPUT_FILE $OUTPUT_FILE