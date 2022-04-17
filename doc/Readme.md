# Documentación

## Como usar el compilador

Para compilar un fichero de COOL se puede usar el comando:

```
python3 coolc.py "path/to/file.cl"
```

Este compila el fichero `file.cl` y almacena el código generado en un fichero del mismo nombre pero pero con extension `.mips`.

Se pueden consultar las demás opciones de la línea de comandos para el compilador ejecutando `python3 coolc.py -h`.

```
usage: coolc.py [-h] [--out OUT] [--run | --no-run] [--verbose | --no-verbose] file

positional arguments:
  file                  COOL source file.

optional arguments:
  -h, --help            show this help message and exit
  --out OUT             Name for .mips generated file after compilation.
  --run, --no-run       Execute the file compiled with SPIM. (default: False)
  --verbose, --no-verbose
                        Verbose output. (default: False)
```

- `--out`: modifica el fichero de salida para el `.mips` generado, que por defecto es creado con el mismo nombre del fichero de COOL.
- `--run`: facilita la ejecución del programa escrito en COOL ejecutando automáticamente el fichero `.mips` de salida. Para realizar dicha acción es necesario tener `spim` instalado y en el path.
- `--verbose`: imprime en consola el AST generado después de concluido el análisis lexico, parsing y análisis semántico, asi como el código intermedio (CIL) generado previamente a la generación de código final. 

## Requerimientos

### Ambiente de ejecución

El proyecto fue desarrollado y probado bajo un ambiente en `Python 3.9.5`, asi que se espera compatibilidad con esta version y superiores (`3.9+`). No se garantiza la correctitud del compilador o que este sea ejecutable en versiones inferiores.

### Dependencias

La única dependencia del compilador es `ply==3.11`, la cual puede ser instalada ejecutando el comando `python3 -m pip install ply==3.11`.
