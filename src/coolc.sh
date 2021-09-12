# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "cool-compiler-2021"
echo "Copyright (c) 2021: Reinaldo Barrera Travieso"

# Llamar al compilador
python3 main.py $INPUT_FILE $OUTPUT_FILE