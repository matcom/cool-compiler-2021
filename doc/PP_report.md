
# Prácticas de producción: Cool-compiler-2021

## Reinaldo Barrera Travieso C411  

La evaluación de la asignatura Complementos de Compilación, inscrita en el programa del 4to año de la Licenciatura en Ciencia de la Computación de la Facultad de Matemática y Computación de la
Universidad de La Habana, consiste este curso en la implementación de un compilador completamente
funciónal para el lenguaje _COOL_.

_COOL (Classroom Object-Oriented Language)_ es un pequeño lenguaje que puede ser implementado con un esfuerzo razonable en un semestre del curso. Aun así, _COOL_ mantiene muchas de las características de los lenguajes de programación modernos, incluyendo orientación a objetos, tipado estático y manejo automático de memoria.

Este proyecto se va a dividir en 4 fases:

* Lexer
* Parser
* Semantica
* Generación de código
  
### Lexer

La fase del lexer donde se va a convertir el código de entrada en una lista de token fue implementada usando la bibloteca de python ```ply.lex```, donde esta nos brinda todas las herraminetas necesarias y que nos facilita esa parte del compilador donde solo es necesaria mediante expresiones regulares denotar la sintaxis que va usar cada token. Una vez que se le aplica el lexer al código fuente ya podemos pasar a la siguiente fase con la lista de tokens.

Actualemnte esta fase del proyecto ya fue completada parcialmente, obteniéndoces un 100% de efectividad en los test propuestos.

### Parser

En la fase del parser al igual que en la fase anterir se empleó la biblioteca de python ```ply.yacc```. En este caso y de fomra inicial se crea una gerarquía de tokens que indica el orden de procedencia de las expresiones. Luego se procede a definir la gramática que va a ser la base del lenguaje cool apoyándonos de toda la información que aparece en el manual de cool. Esta fase se encuentra completada con un 100% de aceptación en los test propuestos. Una vez finalizada esta fase además de detectar todos los posibles errores de parse se obtiene el AST(árbol de sintaxis abstracto) el cual nos permite avanzar a la siguiente fase.

###Semántica

En esta fase se van a definir todas las reglas semánticas de nuestro compilador, este consiste en hacer varios recorriodos por el AST apoyándonos en el patron ```visitor``` donde cada uno tiene una funcionalidad diferente y se dividen de la siguiente manera.

* Type Collector
* Type Builder
* Type Check

**Type Collector:**  
 Este recorrido nos va permitir obtener todos los typos, por tanto aquí solo se va a llegar hasta los nodo de las clases (```ClassNode```). Por cada clase se va a crear un nuevo tipo con los nombres de cada clase. En el caso de los built-in, se van a obtener al compilar un archivo *.cl* ya definido con todo el código.

**Type Builder**

En este recorrido se van a construir los tipos definidos en el código por lo que el recorrido solo va a llegar hasta los nodos de los métodos y los atributos (```MethodNode``` y ```AttributeNode```) donde aquí se va a tomar toda la información necesaria, como sería el caso de nombre de métodos que forma la clases con sus respectivos argumentos, al igual que todos los atributos.

**Type Check**

En este último recorrido se va a analizar todos los nodos del AST donde se va a definir todas las reglas semánticas faltantes como el buen funcionamiento del lenguage, todas estas reglas se presentan en el manual de cool.

A pesar de que esta última fase tiene un 100% en los test de prueba propuesto aún quedan errores semánticos que detectar, y en una planificación esta sería finalizado para finales de Septimebre principio de Octubres.

### Generación de código 

Esta última fase del proyecto se realizaría de octubre a principos de diciembre incluso un poco antes, en el caso que se finalice con antelación la fase anterior. 