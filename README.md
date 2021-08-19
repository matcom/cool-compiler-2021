## Proyecto de compilación



#### Integrantes: Richard Garcia De la Osa C412, Andy Castañeda Guerra C412



#### Bicliotecas usadas:

​	En nuestro proyecto utilizamos la biblioteca **ply** para generar el **lexer** y el **parser** para la gramática de **Cool**.



#### Fases del proyecto:

​	Primeramente desarrollamos el lexer, apoyándonos de **ply.lex**, así como de la documentación del mismo.

​	Una ventaja de trabajar con esta librería es que además, nos permite crear fácilmente el parser para nuestra gramática, apoyándonos en el lexer anteriormente creado. Para esto usamos **ply.yacc**, lo cual nos devuelve un **AST** con la estructura que deseemos.

​	Al contar ya con el **AST**, realizaremos 5 recorridos sobre el mismo, estos son:

* Type Collector: para registrar todos los tipos con los que trabajaremos en el programa.
* Type Builder: encargado de agregarle a cada uno de los tipos anteriormente colectados cada una de sus funcionalidades(atributos, funciones).
* Type Checker: con este recorrido nos aseguramos que la semántica del programa se corresponda con la semántica esperada para Cool. A partir de este punto el código no contiene ningún error.
* Code Gen: fase de generación de código, contenido por estudiar.
* Executor: ejecutar finalmente el programa.



​	Pretendemos para septiembre tener finalizado el lexer, el parser, y los tres primeros recorridos enunciados, TypeCollector, TypeBuilder y TypeChecker. Para los meses restantes, pretendemos en octubre ya tener la fase de generación de código implementada. Luego en noviembre solo restaría la ejecución, y en el tiempo restante, dedicarnos a pulir errores.