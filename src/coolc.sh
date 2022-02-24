# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "Cool Compiler v1.0"        
echo "Copyright (c) 2019: Richard García De la Osa, Andy A. Castañeda Guerra" 

# Llamar al compilador
# echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
exec python3 main.py $INPUT_FILE
