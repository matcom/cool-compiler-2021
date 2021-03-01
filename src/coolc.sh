# Incluya aquí las instrucciones necesarias para ejecutar su compilador
#
INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips
#
# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "coolc 0.1.0"
echo "Copyright (c) 2019: Alejandro Klever Clemente, Laura Tamayo Blanco, Miguel Angel Gonzalez Calles"
#
# Llamar al compilador
# echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
python cool run $INPUT_FILE