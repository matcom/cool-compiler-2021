# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
#OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "Cool Compiler 2021 v1.0"                            # TODO: Recuerde cambiar estas
echo "Copyright (c) 2019: Miguel Asin, Gabriel Martin"    # TODO: líneas a los valores correctos

# Llamar al compilador
#"Compiling $INPUT_FILE into $OUTPUT_FILE"

python3 Compiler/compiler.py $INPUT_FILE
