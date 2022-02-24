# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "codersUP - COOLCompilerv0.0.1"
echo "Copyright (c) 2022: Carmen Irene Cabrera Rodríguez, David Guaty Domínguez, Enrique Martínez González"
# Llamar al compilador
python3 main.py -f "$INPUT_FILE"
