
# Practicas de produccion: Cool-compiler-2021

## Reinaldo Barrera Travieso C411  

La evaluación de la asignatura Complementos de Compilación, inscrita en el programa del 4to año de la Licenciatura en Ciencia de la Computación de la Facultad de Matemática y Computación de la
Universidad de La Habana, consiste este curso en la implementación de un compilador completamente
funcional para el lenguaje _COOL_.

_COOL (Classroom Object-Oriented Language)_ es un pequeño lenguaje que puede ser implementado con un esfuerzo razonable en un semestre del curso. Aun así, _COOL_ mantiene muchas de las características de los lenguajes de programación modernos, incluyendo orientación a objetos, tipado estático y manejo automático de memoria.

Este proyecto se va a dividir en 4 fases:

* Lexer
* Parser
* Semantica
* Generacion de codigo
  
### Lexer

La fase del lexer donde se va a convertir el codigo de entrada en una lista de token fue implementada usando la bibloteca de python ```ply.lex```, donde esta misma nos brinda todas las herraminetas necesarias y que nos facilita esa parte del compilador donde solo es necesaria mediantes expresiones regulares denotar la sintaxis que va usar cada token. Una vez que se le aplica el lexer al codigo fuente ya podemos pasar a la siguiente fase con la lista de tokens.

Actualemnte esta fase del proyecto ya fue completada parcialmente, obteniendoces un 100% de efectividad en los test propuestos.

### Parser

En la fase del parser al igual que en la fase anteriro se empleara una bibloteca de python, en este caso ```ply.yacc```. En este caso y de fomra inicial se crea una gerarquia de tokens que indica el orden de procedencia de las expresiones. Luego se procede a definir la gramatica que va a ser la base del lenguage cool apoyandonos de toda la informacion que aparece en el manual de cool. Esta fase se encuentra completada con un 100% de aceptacion en los test propuestos. Una vez finalizada esta fase ademas de detectar todos los posibles errores de parse se optiene el AST(arbol de sintaxis abstracto) el cual nos permite avansar a la siguiente fase.

###Semantica

En esta fase se van a definir todas las reglas semanticas de nuestro compilador, este consiste en hacer varios recorriodos por el AST apoyandonos en el patron ```visitor``` donde cada uno tiene una funiconalidad diferente y se dividen de la siguiente manera.

* Type Collector
* Type Builder
* Type Check

**Type Collector:**  
En este recorrido nos va permitir obtener todos los typos, por tanto aqui solo se va a llegar hasta los nodo de las clases (```ClassNode```). Por cada clase se va a crear un nuevo tipo con los nombres de cada clase. En el caso de los built-in, se van a obtener al compilar un archivo *.cl* ya definido con todo el codigo.

**Type Builder**

En este recorrido se van a construir los tipos definidos en el codigo por lo que el recorriedo solo va a llegar hasta los nodos de los metodos y los atributos (```MethodNode``` y ```AttributeNode```) donde aqui se va a tomar toda la informacion necesaria, como seria el caso de nombre de metodos que forma la clases con sus respectivos argumentos, al igual que todos los atributos.

**Type Check**

En este ultimo recorrido se va a analizar todos los nodos del AST donde se va a definir todas las reglas semanticas faltantes como el buen funcionamiento del lenguage, todas estas reglas se presentan en el manual de cool.

A pesar de que esta ultima fase tiene un 100% en los test de prueba propuesto aun quedan errores semanticos que detectar, y en una planificacion esta seria finalizado para finales de Septimebre principio de Octubres.

### Generacion de codigo 

Esta ultima fase del proyecto se realizaria de octubre a principos de diciembre incluso un poco antes, en el caso que se finalice con antelacion la fase anteriro. 