# Documentación

## Readme

Modifique el contenido de este documento para documentar de forma clara y concisa los siguientes aspectos:

- Cómo ejecutar (y compilar si es necesario) su compilador.
- Requisitos adicionales, dependencias, configuración, etc.
- Opciones adicionales que tenga su compilador.

## Sobre los Equipos de Desarrollo

Para desarrollar el compilador del lenguaje COOL se trabajará en equipos de 2 o 3 integrantes. El proyecto de Compilación será recogido y evaluado únicamente a través de Github. Es imprescindible tener una cuenta de Github para cada participante, y que su proyecto esté correctamente hosteado en esta plataforma. 

**⚠️ NOTA**: Debe completar el archivo `team.yml` con los datos correctos de cada miembro de su equipo.

## Sobre los Materiales a Entregar

Para la evaluación del proyecto Ud. debe entregar un informe en formato PDF (`report.pdf`) en esta carpeta, que resuma de manera organizada y comprensible la arquitectura e implementación de su compilador.
El documento no tiene límite de extensión.
En él explicará en más detalle su solución a los problemas que, durante la implementación de cada una de las fases del proceso de compilación, hayan requerido de Ud. especial atención.

## Estructura del reporte

Usted es libre de estructurar su reporte escrito como más conveniente le parezca. A continuación le sugerimos algunas secciones que no deberían faltar, aunque puede mezclar, renombrar y organizarlas de la manera que mejor le parezca:

- **Uso del compilador**: detalles sobre las opciones de líneas de comando, si tiene opciones adicionales (e.j., `--ast` genera un AST en JSON, etc.). Básicamente lo mismo que pondrá en este Readme.
- **Arquitectura del compilador**: una explicación general de la arquitectura, en cuántos módulos se divide el proyecto, cuantas fases tiene, qué tipo de gramática se utiliza, y en general, como se organiza el proyecto. Una buena imagen siempre ayuda.
- **Problemas técnicos**: detalles sobre cualquier problema teórico o técnico interesante que haya necesitado resolver de forma particular.

## Sobre la Fecha de Entrega

Se realizarán recogidas parciales del proyecto a lo largo del curso. En el Canal de Telegram se anunciará la fecha y requisitos de cada entrega.


**^^^^^ BORRAR ^^^^^**

## Como usar el compilador

Para compilar un fichero de COOL se puede usar el comando:

```
python3 coolc.py "path/to/file.cl"
```

Este compila el fichero `file.cl` y almacena el codigo generado en un fichero del msimo nombre pero pero con extension `.mips`, ubicado en la carpeta raiz donde se ejecuto el comando.

Se pueden consultar las demas opciones de la linea de comandos para el compilador ejecutando `python3 coolc.py -h`.

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

- `--out`: modifica el fichero de salida para el `.mips` generado, que por defecto es creado con el mismo nombre del fichero de COOL y en la direccion raiz donde se esta ejecutando el compilador.
- `--run`: facilita la ejecucion del programa escriton en COOL ejecutando automaticamente el fichero `.mips` de salida. Para realizar dicha accion es necesario tener `spim` instalado y en el path.
- `--verbose`: imprime en consola el AST generado despues de concluido el analisis lexico, parsing y analisis semantico, asi como el codigo intermedio (CIL) generado previamente a la generacion de codigo final. 

## Requeriemientos

### Ambiente de ejecucion

El proyecto fue desarrollado y probado bajo un ambiente en `Python 3.9.5`, asi que se espera compatibilidad con esta version y superiores (`3.9+`). No se garantiza la correctitud del compilador o que este sea ejecutable en versiones inferiores.

### Dependencias

La unica dependencia del compilador es `ply==3.11`, la cual puede ser instalada ejecutando el comando `python3 -m pip install ply==3.11`.
