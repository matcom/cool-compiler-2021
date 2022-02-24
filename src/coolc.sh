# Incluya aquí las instrucciones necesarias para ejecutar su compilador

INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "EL_COMPI 1.0"
echo "Copyright (c) 2022: Amalia_Ibarra, Sandra_Martos, Gabriela_Martinez"

# Llamar al compilador
exec python3 main.py $INPUT_FILE
