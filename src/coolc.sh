# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "Stranger Bugs Cool Compiler v0.1"
echo "Copyright (c) 2019: Alejandro Klever Clemente, Laura Tamayo Blanco, Miguel Angel Gonzalez Calles"

# Llamar al compilador

if [[ $(pwd) == *src ]] 
then
    python cool compile "${INPUT_FILE}" "${OUTPUT_FILE}"
else
    cd src
    python cool compile "${INPUT_FILE}" "${OUTPUT_FILE}"
fi
