# Informe

El objetivo principal de la aplicación es contruir un compilador que convierta un programa de COOL en un programa funcionalmente equivalente en MIPS. Se mostrará su uso y se describirá la arquitectura y procesos relacionados con su contrucción y funcionamiento.

## ¿Cómo usar el compilador?

### Uso básico

Para el uso del compilador es necesario correr el archivo `src/coolc.sh`. Este compilará el programa COOL que se le dió como entrada y guardará el programa MIPS en la misma localización con extensión _.mips_.

- `$ ./src/coolc.sh <archivo_programa_cool>`

### Uso avanzado

El compilador hecho presenta además otras características que son posibles si se llama al programa
`src/cool_cmp/main.py` estas características son activada mediante diferentes flags que se le pasan al programa:

- `-m`: Guarda el programa compilado a MIPS en el archivo de salida dado con extensión `.mips`
- `-c`: Guarda el programa generado de CIL en el archivo de salida dado con extensión `.cil`
- `-i`: Guarda el progama de COOL con los AutoType resueltos en el archivo de salida dado con extensión `.infer.cil`
- `-icil`: Interpreta el AST de CIL generado por el programa de entrada
- `-icool`: Interpreta el AST de Cool generado por el programa de entrada

Por ejemplo el siguiente programa interpreta y guarda el código CIL generado
> $python3 src/cool_cmp/main.py src/testing.cl src/testing.cil -icil -c

También posee otras características previstas para el desarrollador del compilador:

- `-ucp`: Actualiza el parser serializado de Cool
- `-ucl`: Actualiza el lexer serializado de Cool

## Arquitectura

### Estructura

El compilador se divide en tres módulos principales:
- cmp: 
  - Clases bases de la API de Gramática
  - Implementación del patrón visitor
  - Clases bases para herramientas de análisis semántico
  - Nodos bases de AST de Cool y CIL
- cmp_tools:
  - Implementación de lexer
  - Implementación de parsers
- cool:
  - Gramática, parser, lexer, AST de Cool
  - Implementación de los visitors del compilador.

TODO tal vez se creen nuevos módulos en relación a los diferentes lenguajes en el proyecto por ejemplo ahora esta solamente cool, pero ahí se mezcla con cil, si se separan estos sería un poco más organizado el proyecto, y luego vendría mips. Finalmente quedarían además de los que ya están **cil** y **mips**

### Flujo de trabajo

La dinámica de flujo de trabajo del compilador se ve repressentada por tubos y tuberías (Pipe, Pipeline), las cuales permiten una gran flexibilidad y desacomplamiento a la hora de agregar pasos en el proceso a seguir.

TODO Alguna foto explicativa de los pipes y pipelines

Gracias a esto es posible crear y tener diferentes flujos de trabajo para usarlos fácilmente. Por ejemplo en el proyecto se tienen varios flujos de trabajo listos para su uso:
- `generate_cil_pipeline`: Genera el código CIL correspondiente al programa COOL que se dió de entrada.
- `generate_cool_pipeline`: Reconstruye el programa COOL de entrada con los tipos inferidos sustituídos
- `interprete_cool_pipeline`: Interpreta el programa COOL en Python. 

#### Errores

Detectar y mostrar los errores son un paso crucial en cualquier aplicación que permite al usuario ahorrar mucho tiempo al proveerle una descripción lo más precisa posible de este. El flujo principal de la aplicación posee una lista, la cuál contiene todos los errores incurridos por etapas anteriores. Al final de la ejecución los errores son escritos en la salida estándar del programa. 

En la implementación de los flujos, generalmente se ignora realizar una fase si existe algún error previo, por esto se asume en las explicaciones que siempre se llega a ellas sin errores previos.

### Fases

El compilador se divide en dos fases principales:
- Fase de análisis: Empieza leyendo el código fuente (COOL) y termina en la construcción de un AST de código intermedio (CIL)
- Fase de síntesis: Empieza recibiendo el AST de código intermedio y termina en la generación de código MIPS.

La segunda fase puede que se omita en caso de que lo que se quiera no necesite generar código MIPS, un ejemplo de esto es cuando se quiere interpretar COOL.

### Fase de análisis

En la fase de análisis se contemplan las siguientes etapas:
1. Lectura del programa
2. Tokenización del programa
3. Análisis sintáctico
4. Análisis semántico
5. Acción correspondiente a la entrada (Construir AST CIL, Interpretar COOL, etc)

#### Tokenización

Este proceso es el encarado de convertir el texto plano de un programa de COOL en una lista de tokens para poder trabajar con ellas en próximas etapas.

Siguiendo el flujo de trabajo propuesto, esta etapa se realiza usando el pipe `lexer_pipeline` en la cual se lee el texto y se tokeniza usando el módulo `ply` y se añade la lista de tokens resultante al flujo.

En este paso también se ignoran los comentarios en la salida de los tokens ya que estos no son necesarios para el análisis semántico. Un problema que se pudo apreciar en esta etapa es que los comentarios anidados no pueden ser eliminados con expresiones reglares ya que estas fallan al identificar este tipo de estructuras, para resolver este problema se (TODO WATA Como fue que se resolvió esto). 

#### Análisis sintáctico

Este proceso es el encargado de convertir los tokens del programa en un árbol de sintaxis abstracta, en caso de que estos coincidan con la gramática del lenguaje.

El pipeline encargado de esta etapa es `syntax_pipeline` el cual evalúa el parser con los tokens dados y añade al flujo la derivación de extrema derecha de los tokens que luego será evaluada y convertida en un AST por la gramátca atributada.

##### Gramática

La gramática propuesta para COOL se encuentra en `cool/grammar/cool_grammar.py`. Esta es una gramática atributada la cual al ser evaluada devuelve el AST correspondiente al programa de entrada de COOL.

##### Parser

El parser es contruído en base a la gramática previamente definida, este consiste en un parser LALR1. Ya que su construcción dinámica incurre en un consumo de tiempo relativamente alto, este se encuentra serializado para un mejor rendimiento del inicio del programa.

#### Análisis semántico

Este proceso es el encargado de verificar la correcta semántica del programa de COOL. Se aplica fuertemente el patrón visitor, pasando por diferentes etapas las cuales van construyendo diferentes estructuras y analizando el contenido del AST para verificar su correctitud.

El pipeline encargado de esta etapa es `semantic_pipeline`.

##### Construcción del Contexto

El contexto de un programa de COOL se puede definir como una colección de los tipos que están definidos en el programa. Estos tipos tiene otras informaciones como son los atributos, métodos y padre. La construcción del contexto pasa por tres etapas:

1. Construcción del contexto inicial (Contexto que posee la información de las clases básicas Ej: Object, Int).
2. Recolección de tipos y construcción del árbol de dependencias.
3. Construcción de tipos.

Para la construcción del contexto inicial se creó un esqueleto contentiendo las definiciones de las clases bases con sus respectivos métodos (ver `cool/lib/std.cool`). Este esqueleto es analizado por la infraestructura existente y devuelve el contexto inicial. Se prefirió esta aproximación ya que permite obtener el contexto de forma natural sin tener que recurrir a tenerlo fijado dentro del código.

La recolección de tipos constituye el paso en el que se agregan los tipos definidos al contexto del programa, en esta etapa se comprueba que no existan ciclos en la relación de padre de los tipos.

Finalmente se agrega la información restante a los tipos como son los métodos y atributos que los conforman.

##### Comprobación de tipos y construcción del ámbito

Una vez se tiene el contexto contruído es necesario verificar las demás reglas semánticas de COOL. En esta etapa se:

- Se anotan los nodos que contienen tipos con las expresiones correspondientes.
- Se construye el ámbito (Scope) del programa.
- Comprueban las reglas semánticas de COOL.

Para realizar el chequeo de tipos de un programa de COOL es necesario conocer el tipo estático de las expresiones, esto se realiza con un recorrido del AST de COOL en post-orden anotando el tipo de las expresiones de manera bottom-up para comprobar la correctitud de las operaciones entre estas. En el mismo recorrido se va construyendo el Scope que verifica la correctitud en el uso de variables. También se verifican las demás reglas semánticas como por ejemplo las relacionadas con la sobreescritura de métodos. 

##### Tipo especial SELF_TYPE

TODO Ver si funciona bien y como es que se trabaja en el análisis semántico

##### Inferencia de tipos

El proyecto soporta inferencia de tipos mediante la anotación del tipo con el nombre especial de AUTO_TYPE. 

El algoritmo propuesto para la inferencia de los tipos AUTO_TYPE se basa en la idea de ir 
descartando los tipos que no pueden ser, basándose en las operaciones realizadas sobre los 
AUTO_TYPE y las operaciones válidas sobre los posibles tipos. Estas operaciones pueden ser 
asignación, operaciones aritméticas y despachado de métodos. Luego que se tiene toda la 
información necesaria, se comprueba que no haya incoherencias en los posibles tipos 
resultantes (Ej: métodos con igual nombre y parámetros en clases no relacionadas) y se 
sustituye en los nodos del AST, el AUTO_TYPE, por el tipo el más adecuado según su posición 
(Ej: argumentos el más abstracto, en tipo de retorno el más concreto). 
 
La primera parte del algoritmo consiste en reunir toda la información sobre las operaciones que 
actúan sobre los AUTO_TYPE, esto se hace de manera automática en el chequeo de tipos 
mediante la llamada a los métodos conforms_to, get_attribute y get_method de la clase 
AutoType y operation_defined de Operator. Estos métodos son llamados en el recorrido 
TypeChecker para comprobar que las operaciones a realizar sobre los tipos cumplen las reglas 
semánticas. El algoritmo se aprovecha de esto y elimina en esta etapa los tipos que no 
satisfacen las operaciones (Vea cool.semantic.type.AutoType y 
cool.semantic.operations.Operator.operation_defined).  
La segunda parte consiste en verificar la validez de los posibles tipos. Definimos a un 
AUTO_TYPE como válido si el grafo de sus posibles tipos (tomando la relación A padre de B) es 
unilateralmente conexo y no vacío. Esta definición se debe a que en caso de no ser 
unilateralmente conexo, significaría que habría dos sub herencias disjuntas que podrían ocupar 
el lugar del AUTO_TYPE y en este caso no se podría decidir entre una de estas. Por otra parte en 
el caso de ser vacío significaría que no hay posibles tipos que satisfagan las operaciones 
realizadas sobre el AUTO_TYPE. Una vez comprobada la validez del AUTO_TYPE se pone a los 
nodos el tipo correspondiente a su posición ya sea el más abstracto o concreto. Esta segunda 
parte se realiza en el recorrido AutoResolver. Ejemplos de casos válidos (Izquierda) y no válidos 
(Derecha): 

TODO: Poner las fotos del informe del segundo proyecto

#### Fin del análisis semántico

Al final del análisis semántico se sabe que el programa es correcto o no y se tiene un AST de este listo para ser procesado según haga falta. 

##### Interpretar COOL

Este árbol es posible interpretarlo, para esto se creó un visitor que ejecuta los nodos en el mismo Python. Esto es útil a la hora de verificar la correctitud del código sin tener que compilarlo y aumentar las probabilidades de que el error sea otro.

##### Convertir AST COOL a AST CIL

TODO Seguir con esto
La conversión del AST de COOL al de CIL se realiza en una sola pasada al árbol.
- Para instanciar nuevos tipos se generaron nuevas funciones inicializadores ejecutan las funciones necesarias para ponerle los valores iniciales a los atributos.


### Fase de síntesis
TODO 

