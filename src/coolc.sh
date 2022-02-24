INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "Cool Compiler v1.0"
echo "Copyright (c) 2022: Luis Lara , Carlos Arrieta"

# Llamar al compilador
python3 main.py ${INPUT_FILE}
