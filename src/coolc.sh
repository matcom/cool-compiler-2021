# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "Cool Compiler 2021 v1"        # TODO: Recuerde cambiar estas
echo "Copyright (c) 2021: Alejandro Campos, Darian Dominguez"    # TODO: líneas a los valores correctos

FILE="main.py"

# Llamar al compilador
python ${FILE} $INPUT_FILE $OUTPUT_FILE
