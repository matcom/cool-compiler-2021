# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "COOLCompiler_v1.0"        # TODO: Recuerde cambiar estas
echo "Copyright (c) 2021: Karla Olivera, Amanda Gonzalez, Victor Cardentey"    # TODO: líneas a los valores correctos


exec python3 cool.py $INPUT_FILE