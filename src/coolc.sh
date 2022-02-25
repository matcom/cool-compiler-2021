# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
# echo "COOL COMPILER 3.2v"
echo "Copyright (c) 2021: Juan Carlos Vazquez Garcia, Yandy Sanchez Orosa"

# Llamar al compilador
echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
python3 main.py $INPUT_FILE
