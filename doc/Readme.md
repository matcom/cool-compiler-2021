# Documentación

**Nombre** | **Grupo** | **Github**
--|--|--
Laura Brito Guerrero | C412 | [@LauryGirl](https://github.com/LauryGirl)
Sheyla Cruz Castro | C412 | [@sheycc](https://github.com/sheycc)
Ariel Antonio Huerta Martín | C412 | [@huertaariel1](https://github.com/huertaariel1)

# Uso del compilador

Para utilizar el compilador es necesario instalar todas las dependencias utilizadas por este como
son los paquetes `ply` para la generación del lexer y el parser, y para la ejecución de los tests, `pytest`
y `pytest-ordering`, todo esto se logra ejecutando el fichero `requirements.txt` de la forma: 

```bash
pip install -r requirements.txt
```

Para ejecutar el compilador es necesario correr el archivo ```cool.sh``` ubicado en `/src/` dando como entrada la dirección del archivo a compilar de la siguiente forma:

```bash
cd src/
./cool.sh '../tests/codegen/arith.cl'
```

El archivo principal del compilador es `main.py`, módulo que contiene toda la lógica del compilador, si desea ejecutarlo debe pasar como argumento el `path` del fichero **.cl** con código fuente de COOL que se desea compilar, de la siguiente forma:

```bash
python3 main.py '../tests/codegen/arith.cl'
```

Un archivo en el mismo path del código fuente será creado, con el mismo nombre, pero con extensión **.mips** que puede ser ejecutado con **spim**.

Para ejecutar las pruebas localmente, debe tener instalado `Python 3.7`, `pip` y `make` que normalmente viene incluido en Linux, para hacerlo ejecute los siguientes comandos:

```bash
cd src/
make clean
make test
```