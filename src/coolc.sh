# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "CoolCow 0.1"        # TODO: Recuerde cambiar estas
echo "Copyright (c) 2021: Adrian, Rodrigo"    # TODO: líneas a los valores correctos

# Llamar al compilador
# echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

exec python3 __main__.py $INPUT_FILE 