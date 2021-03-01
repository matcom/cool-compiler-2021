#!/bin/bash

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "CMA COOL COMPILER v1.0"        # TODO: Recuerde cambiar estas
echo "Copyright (c) 2019: Marcos Valdivie, Claudia Olavarrieta, Adrian Hernandez"    # TODO: líneas a los valores correctos

# Llamar al compilador

#echo "Compiling $INPUT_FILE into $OUTPUT_FILE"
python3 Main.py -f $INPUT_FILE