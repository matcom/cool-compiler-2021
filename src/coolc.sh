# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "Version 1.0 cool-compiler-2021"
echo "Copyright (c) 2019: Thalia Blanco, Nadia Gonzalez, Jose A. Labourdette"

# Llamar al compilador
#echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

python main_.py $INPUT_FILE
