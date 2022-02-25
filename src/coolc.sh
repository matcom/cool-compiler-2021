# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips
BASEDIR=$(dirname "$0")
PROGRAM=$BASEDIR/cool_cmp/main.py

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "WLD CoolCompiler v0.0"
echo "Copyright (c) 2019: Luis Ernesto, Damián, Luis Enrique"

# Llamar al compilador
# echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

python3 $PROGRAM $INPUT_FILE $OUTPUT_FILE -m