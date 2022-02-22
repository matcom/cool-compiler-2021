# Incluya aquí las instrucciones necesarias para ejecutar su compilador

# Si su compilador no lo hace ya, aquí puede imprimir la información de contacto
echo "Coolpyler 0.1"
echo "Copyright (c) 2019: Jorge Mederos Alvarado, Rodrigo García Gómez"

# Llamar al compilador
PYTHONPATH="$(dirname $0)" python -m coolpyler $@
