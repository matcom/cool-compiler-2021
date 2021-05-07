# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "Cool Compiler version 1.0"        # TODO: Recuerde cambiar estas
echo "Copyright (c) 2021: Laura Brito Guerrero, Sheyla Cruz Castro, Ariel Huerta Martin"    # TODO: líneas a los valores correctos

# Llamar al compilador
python3 main.py $INPUT_FILE
