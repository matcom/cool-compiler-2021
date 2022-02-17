# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto 
echo "AnotherCoolTeamCompiler"   # TODO: Recuerde cambiar estas
echo "Copyright (c) 2021: Yasmin Cisneros Cimadevila & Jessy Gigato Izquierdo"    # TODO: líneas a los valores correctos

# Llamar al compilador
python3 pipeline.py final_execution "${INPUT_FILE}" "${OUTPUT_FILE}"


if [[ $(pwd) == *src ]] 
then
    python3 pipeline.py final_execution "${INPUT_FILE}" "${OUTPUT_FILE}"
else
    cd src
    python3 pipeline.py final_execution "${INPUT_FILE}" "${OUTPUT_FILE}"
fi
