# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "Cool Compiler v0.1"
echo "Copyright (c) 2022: Carlos Alejandro Arrieta Montes de Oca, Luis Alejandro Lara Rojas"

# Llamar al compilador
python3 main.py ${INPUT_FILE}
