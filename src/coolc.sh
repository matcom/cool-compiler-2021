# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "COOL Compiler v0.1.0"
echo "Copyright (c) 2019: Javier A. Valdes, Yansaro R. Paez, Osmany"

# Llamar al compilador
echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
