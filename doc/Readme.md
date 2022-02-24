# Documentación

## Uso del compilador

El presente compilador fue desarrollado en el sistema operativo Ubuntu 20.4, donde se utilizo Python 3.8.10 como lenguaje de programación.

El proyecto en general tienen los siguientes requerimientos iniciales para su ejecución:
• ply
• pytest
• pytest-ordering

Para instalar todas las dependencias basta con ejecutar el siguiente comando en el directoria de raı́z:

```bash
$ pip install -r requirements.txt
```

En particular como todo el proyecto fue realizado en python3, también cabe destacar que para los test de prueba se debe emplear la herramienta
pytest3. Por otra parte, para instalar las dependencias también se debe usar el comando pip3.

**NOTA**: El compilador no fue probado en versiones anteriores de python por lo que no se tiene conocimientos de su correcto funcionamiento.

##Estructura del proyecto

.
├── CIL  
│   ├── ast.py  
│   ├── cil.py   
├── coolc.sh  
├── main.py  
├── makefile  
├── MIPS  
│   ├── mips.py     
├── Parser  
│   ├── ast.py  
│   ├── lexer.py  
│   ├── parser.out  
│   ├── parser.py  
│   ├── parsetab.py  
├── Semantic  
│   ├── builder.py  
│   ├── checker.py  
│   ├── collector.py  
└── Tools  
    ├── context.py  
    ├── errors.py  
    ├── messages.py  
    ├── scope.py  
    ├── tokens.py  
    ├── utils.py  
    └── visitor.py  

## Compilando su proyecto
Una vez dentro de la carpeta cool-compiler-2021 se abre una terminal y se ejecutan los siguientes comandos :

```bash
$ cd src
$ make clean
$ make
```

El primer comando es el encargado de cambiar el directorio actual al directorio source, en donde se encuentra el fichero principar para ejecutar el compilador. Este comando puede ser ignorado si la terminal se abre desde el directorio source.

El segundo comando el el encargado de limpiar toda las basura y residuos que pueden quedar dentro de la estructura de ficheros de las ejecuciones
anteriores.

Por último el tercer comando es el encargado de compilar el resultado final, para este caso este comando es innecesario pues la ejecución del compilador no depende de una compilación previa, pues este se ejecuta directamente desde consola con python. Por este motivo este comando solo mostrara un mensaje simbólico al usuario.

## Ejecutando su proyecto

En el proyecto se incluye el archivo /src/coolc.sh el cual es el encargado de ejecutar el compilador. Este muestra inicialmente un mensaje con el nombre del compilador y los nombres de los autores, seguido de esto se pasa a ejecutar las instrucciones pertinente. Al ejecutar este archivo se debe pasar un argumento que seria el nombre del fichero que se quiere compilar. Para un mejor visualización en la terminal se debe ejecutar el siguiente comando:

```bash
$ ./coolc.sh <input_file.cl>
```

El argumento <input file.cl> especifica el nombre del fichero, y como se trata de un compilador del lenguaje COOL la extensión de este siempre debe ser un .cl. Una vez terminado el proceso de compilación la salida de este es otro fichero de igual nombre pero ahora con la extensión .mips. Otro forma de ejecutar el compilador es mediante el siguiente comando:

```bash
python3 main.py <input_file.cl> <output_file.mips>
```

Si se fijan en este caso, se debe pasar tanto el fichero de entrada como el fichero de salida, lo cual puede traer algunas consecuencia a la hora de pasar incorrectamente los argumentos. Para el caso del fichero de entrada puede suceder que no se escriba bien el nombre del mismo o que se le de una extensión no permitida, lo cual puede terminal en errores del programa a la hora de la ejecución.
