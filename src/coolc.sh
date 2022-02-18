# Incluya aquí las instrucciones necesarias para ejecutar su compilador

COOL_FILE=$1
CIL_FILE=${COOL_FILE:0: -2}cil
MIPS_FILE=${COOL_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "cool-compiler-2021"
echo "Copyright (c) 2021: Reinaldo Barrera Travieso"

# Llamar al compilador
python3 main.py $COOL_FILE $CIL_FILE $MIPS_FILE