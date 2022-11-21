# Reporte

### Integrantes

#### Yasmin Cisneros Cimadevila ---- C511
#### Jessy Gigato Izquierdo ---- C511
--------------------

# Arquitectura del Compilador

La estructura del compilador la modelamos de la siguiente manera:
- Tokenizador
- Parser (en este se genera el AST)
- Proceso de Semántica:
    - Colector de tipos
    - Constructor de tipos
    - Analisis de dependencia cíclica
    - Chequeo de tipos
- Generación de Código:
    - Transformacion del AST
    - AST COOL-CIL
    - AST CIL-MIPS
    - Generación del archivo .mips 


## Tokenización y Parser
Para la construcción del lexer y el parser se utiliza la biblioteca `ply` de python, que provee herramientas para la generación del AST a partir de una gramática. El método de parseo utilizado fue `LALR`.

## Semántica
Del proceso de análisis de la semántica se obtiene un nuevo AST en el que cada una de sus ramas ha adquirido el significado semántico que debe tener, es decir, se asegura de que se cumplan las reglas definidas que asignan un significado lógico a las expresiones dadas por la sintaxis del lenguaje.
La evaluación de las reglas semánticas define los valores de los atributos de los nodos del AST para la cadena de entrada. Para el caso de los operadores, cada nodo de este tipo, al terminar el análisis sabe si la operación asociada es aplicable o no.
En el colector y constructor de tipos se recopilan los mismos, tanto los existentes en el lenguaje como los creados por las clases definidas en el código de entrada, y por último en el chequeo de tipos se comprueba si en el contexto dado puede ser utilizado.



## Generación de Código

En este punto ya tenemos un AST sintáctica y semánticamente correcto, y que quiere generar un programan en MIPS equivalente al código de entrada que COOL.

Transformación del AST:\
Primeramente se hacen modificaciones en el AST actual agregando una nueva funcionalidad en la que los atributos declarados pero no asignados que no perteneden a un tipo build-in (Int, Str, Bool) se les asigna una expresión nula, también en este se le asigna un constructor a las clases con el cual posteriormente se realizará la inicialización de la instancia de clase requerida
Como pasar de COOL a MIPS directamente resulta complicado, se pasa primero del AST de COOL a un AST de CIL y luego a partir de este último se construye un AST de MIPS a partir del cual se obtiene un archivo `.mips` listo para ser ejecutado. 

AST COOL-CIL:\
La necesidad principal de tener un lenguaje intermedio es facilitar la trasformacion del código al lenguaje final (MIPS) ya que este no presenta definiciones para tipos y atributos sino solamente muestra una serie de instrucciones que deben de ser ejecutadas en búsqueda de un resultado final por tanto CIL nos sirve de puente entre nuestro lenguaje de entrada (COOL) y el lenguaje de salida (MIPS). Ademas este hace menos engorrosa la búsqueda de errores en la realizacion del mismo.
Un ejemplo donde se evidencia la utilidad de este puente es en caso del CaseNode ya que el lenguaje MIPS no presenta nada parecido a esta clausula por tanto este debe de pasar por un algoritmo que realice una búsqueda de tipos y semejanzas entre ellos para obtener el resultado final, en caso de que no existiera CIL seria complicadisimo lograr una compatibilidad.

AST CIL-MIPS: \
Luego de lograr una reducción intermedia del lenguaje hacia CIL se convierten cada uno de los nuevos nodos de este AST en un conjunto de intrucciones que seran llevadas directamente a lenguaje MIPS

### Puntos a destacar a nivel de implementación:
Manejo de la memoria:\
El manejo de la memoria se realiza mediante el convenio de C, este hace creer a cada uno de los métodos que es dueño del stack

La sección de .data se encuentran contenidos los diferentes tipos con la siguiente estructura:\
tipo del objeto\
padre\
nombre de la direccion\
contructor\
metodos...

El contructor es de gran ayuda ya que ayuda a alijerar código llamando a su etiqueta correspondiente cuando necesite crear una instancia de la clase en cuestión.
