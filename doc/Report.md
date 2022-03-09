## Introducción

Cool(Classroom Object-Oriented Language) es un lenguaje de programación orientado a
objetos que, aunque pequeño, tiene muchas caracterı́sticas relevantes de lenguajes modernos. Su orientación a objetos, su tipado dinámico y el resto de sus features lo hacen muy atractivo e ideal para un primer acercamiento al mundo de los Compiladores. 

En el presente trabajo se muestra una implementación de un Compilador funcional para Cool en el lenguaje de programación python:  *El Compi*. 

En las próximas secciones se explican en detalle cada una de las fases en las que se divide el trabajo del mismo, como fue abordada cada una, las instrucciones para su uso y algunos otros detalles importantes a resaltar.


## Instrucciones para la ejecución

Para utilizar *El Compi* y ejecutar un programa en el lenguaje cool se han de seguir los siguientes pasos:

1- Primero se debe verificar que se cuente con todas las dependencias necesarias. Para una rápida instalación de estas se puede ejecutar el comando:

```bash
$ pip install -r requirements.txt
```

2- Para compilador un código dado en Cool a ensamblador, ejecute:

```bash
$ ./coolc.sh <path_to_file/file_name.cl>
```
en una consola centrada en el directorio *src* que se encuentra en la raiz del proyecto. Aquí <file_name.cl> sería un archivo escrito en cool. 

3- El *output* esperado es un archivo con el mismo nombre pero en .mips, el cual debe correrse con el correspondiente intérprete:

```bash
$ spim -file <path_to_file/file_name.mips>
```
que finalmente nos mostrará el resultado correspondiente al programa de entrada (spim se encuentra entre los requirements especificados).


## Arquitectura del compilador: 

*El Compi*, para tener la funcionalidad completa de un compilador, transita por las fases fundamentales de:

-Análisis sintáctico (Análisis léxico y parsing)

-Análisis semántico

-Generación de código (Generación de un lenguaje intermedio y traducción a mips)

Más adelante se analizan con más profundidad cada una.

El código fuente del proyecto se encuentra en la carpeta *src*. En esta se hallan distribuidos los scripts según su funcionalidad. 

**FOTO  de los archivos del proyecto**

Si lo miramos como módulos, podemos decir que el módulo de lexe... en *code_gen* encontramos todo lo referente al proceso de generación de código...

**COMPLETAR**

Analicemos ahora los prometidos detalles de implementacion y diseño del compilador tan anunciados. 

## Gramática
El primer paso para acercarnos al lenguaje objeto de análisis fue definir una gramática adecuada. Siguiendo lo referido por el manual de Cool (el cual se encuentra adjunto en la carpeta *doc*, con el resto de la documentación), se utilizó una gramática que respetara la precedencia necesaria de los operadores y la estructura requerida. En el archivo cool grammar.py puede observarse como fue modelada la misma. 

Como ahí se puede apreciar, un programa de Cool
consiste en una serie de definiciones de clases. Cada
clase a su vez posee un conjunto de atributos y de fun-
ciones. Las expresiones que pueden formar parte de
dichas funciones son el corazón del lenguaje.
En la imagen *1* se pueden apreciar varios niveles intermedios de la gramática que precisamente definen diferentes tipos de expresiones:

1. <comp>, que representa las operaciones donde se
comparan elementos.

2. <arith>, que engloba a las operaciones de suma y
resta.

3. <term>, para la multiplicación y división.

4. <factor>, como representación de los operadores
unarios isvoid, opuesto y new.

5. <element> para las expresiones entre paréntsis,
los block y las llamadas a funciones.

6. <atom> como el nivel más básico, donde se ex-
cuentran los números, ids, las expresiones boolea-
nas y los strings.

**IMAGEN** Figura 1: Fragmento de la gramática de Cool.

## Análisis sintáctico

### Tokenizer 
Para tokenizar la entrada se utilizó una herramienta bastante útil y práctica: PLY (https://www.dabeaz.com/ply/ply.html), el cual consiste en una implementación en python de las herramientas de parsing les y yaxx. Mediante el módulo lex que esta provee, es posible acceder a un analizador léxico ya implementado.

Para utilizar esta herramienta se definieron una serie de reglas que orientaran al tokenizador como trabajar en las cadenas de entrada. En el archivo
token rules se pueden observar dichas reglas, las cuáles consisten fundamentalmente en definiciones de los patrones que sigue cada token deseado, con la ayuda de expresiones regulares. En este sentido, se
trabajó fundamentalmente con el módulo re de python, el cual permite definir dichas expresiones.

HABLAR DE COMO SE DEFINEN LSO COMENTARIOS
PONER UNA FOTO DE ALGUNA REGLA

Es importante destacar que los tokens de *lex* registran la posición que ocupan en el texto de entrada, considerando el mismo como una array de caracterres. Esto, con la ayuda de una regla para la detección de saltos de línea nos permite tener bien identificada la fila y la columna de un caracter en el script inicial, lo cual es sumamente importante en futuras fases del compilador para ubicar y reportar los errores detectados. 

### Parser

En cambio, para el parser, no fue la variante de ycc la que se decidió utilizar. En este caso, nos mantuvimos fieles a la implementación efectuada por el equipo en proyectos pasados, la cual se puede apreciar en el archivo *shift_reduce* parsers. Este cuenta con las modificaciones pertinentes para adaptarse a los nuevos requerimientos, por ejemplo, para la detección de fila y columna se realiza ahora el parseo sobre tokens del lenguaje, en lugar de sobre simples lexemas.

Con el uso del parser LR1 que aquí se provee y la gramática atributada de *cool_grammar* es posible parsear un texto en cool y obtener un árbol correspondiente a una derivación de extrema derecha.

La construcción de este árbol o ast ($abstract syntax tree$) es la base del resto del análisis que se efectúa por el compilador. A lo largo de la ejecución del proyecto se utilizan una serie de estos árboles, pero primero que se menciona está formado por los nodos que se encuentran en el archivo $ast_nodes.py$.

## Chequeo semántico:

Una vez se tenga un ast con la sintaxis adecuada en mano, la fase siguiente consiste en verificar que el programa en cuestión esté correcto semánticamente.

Con este fin se realizan 3 recorridos sobre el árbol, apoyándonos en el patrón visitor propuesto:

HABLAR DEL CONTEXTO Y DE COMO SE DEFINE
COMO SE REFGISTRA UNA CLASE CON SUS TIPOS BLABLABLA
-TypeCollector: Cuyo objetivo es registrar los tipos definidos por el programa. Aquí sólo se lanza un error cuando se intenta redefinir un tipo, o sea cuando aparece su definición más de una vez en el script propuesto.

-TypeBuilder: Recorrido que busca asignar los métodos y definiciones de atributos a sus clases correspondientes, y detectar errores relacionados con referencias a tipos inexistentes. En este caso es necesario notar que, como Cool permite la herencia, se debe asegurar en este recorrido que no existan ciclos entre las definiciones de clases. Además, para poder garantizar que no se redefinan métodos ni atributos, se asegura que en el momento de definición de un hijo ya se haya visitado al padre, de modo que se tenga constancia de los valores heredados para el análisis.

-TypeChecker: En este último recorrido sí se visitan la totalidad de nodos del ast creado, no sólo los correspondientes a definiciones de clases, métodos o atributos como en las pasadas anteriores. A medida que se recorre el árbol, con el contexto ya populado con las tipos correspondientes al programa y sus propiedades, se va chequeando que se haga un uso correcto de tipos a lo largo de las expresiones utilizadas, que no se referencien variables o atributos inexistentes o fuera de scope, etc, reportando siempre los errores encontrados.

## Generación de código:

### Paso de Cool a CIL:

...
### De CIL de MIPS:
 ...