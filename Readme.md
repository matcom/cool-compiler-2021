# COOL: Proyecto de Compilación

>  Forked from: https://github.com/matcom/cool-compiler-2021, proyecto base para el compilador de 4to año en Ciencia de la Computación.

## Generalidades

La evaluación de la asignatura Complementos de Compilación, inscrita en el programa del 4to año de la Licenciatura en Ciencia de la Computación de la Facultad de Matemática y Computación de la
Universidad de La Habana, consiste este curso en la implementación de un compilador completamente
funcional para el lenguaje _COOL_.

_COOL (Classroom Object-Oriented Language)_ es un pequeño lenguaje que puede ser implementado con un esfuerzo razonable en un semestre del curso. Aun así, _COOL_ mantiene muchas de las características de los lenguajes de programación modernos, incluyendo orientación a objetos, tipado estático y manejo automático de memoria.

## Sobre la implementación

Todo el código e instrucciones necesarias se encuentran en la carpeta `src`. Más información en [`src/Readme.md`](src/Readme.md).

## Sobre la documentación

Se presenta un reporte escrito documentando el proceso de construcción del compilador y los detalles más importantes de su funcionamiento. Más información en [`doc/Readme.md`](doc/Readme.md).

## Sobre los casos de prueba

La carpeta `tests` contiene casos de prueba.

Estos tests se ejecutan automáticamente cada vez que hace un _pull request_ al repositorio `matcom/cool-compiler-2021`. 

Para ejecutar las pruebas localmente, debe tener instalado `Python 3.7`, `pip` y `make` (normalmente viene con Linux). Ejecute:

```bash
$ pip install -r requirements.txt
$ cd src
$ make test
```
