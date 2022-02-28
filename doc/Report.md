# Compilación

### Proyecto Cool Compiler 2021-2022:

##### Integrantes:

-Richard García De la Osa C-412. richard.garcia@estudiantes.matcom.uh.cu.

-Andy A. Castañeda Guerra C-412. andy.castaneda@estudiantes.matcom.uh.cu.



#### Uso del compilador:

Para usar nuestro compilador deberá ejecutar en la consola el siguiente comando:

```bash
bash coolc.sh $INPUT_FILE
```

El archivo __INPUT_FILE__ debe tener extension .cl, correspondiente a un programa del lenguaje Cool.

Este comando generará un fichero con igual nombre pero con extensión .mips, el cual estará listo para ser ejecutado. Para ejecutar el __INPUT_FILE__ (el cual debe tener extensión .mips) deberá usar el siguiente comando en la consola:

```bash
spim -file $INPUT_FILE
```

No hay otros parámetros adicionales para ejecutar nuestro compilador. 

#### Arquitectura del compilador:

El proyecto tiene la siguiente estructura:

###### Módulos:

-lexer: Este módulo está compuesto por __lexer.py__. En este archivo se encuentran las reglas lexicográficas para tokenizar un programa (texto) escrito el __COOL__. Se utiliza la biblioteca __PLY__ de python. 

-c_parser: Este módulo está compuesto por __parser.py__ y __parsetab.py__. En el archivo __parser.py__ están escritas las producciones de la gramática utilizada por nosotros para generar un __AST__ de __COOL__ estructurado a nuestra conveniencia. Por otra parte __parsetab.py__ es un archivo generado por la biblioteca __PLY__ al ejecutar el parser en conjunto con el __lexer.py__ antes mencionado. Este contiene especificaciones sobre el método de parsing utilizado así como los tokens asociados a sus producciones.

-cool_ast: En este módulo se encuentra el archivo __cool_ast.py__ el cual contiene los nodos del __AST__ de __COOL__ que consideramos necesarios para la implementación de nuestro compilador.

-cil_ast: En este módulo se encuentra el archivo __cil_ast.py__ el cual contiene los nodos del __AST__ del código intermedio generado (__CIL__) que utilizamos para traducir el código de __COOL__  a instrucciones sencillas de forma que sea más fácil transformarlo a código __mips__.

-utils: Compuesto por __errors.py__, este contiene el formato de los errores lexicográficos, sintácticos y semánticos que empleamos durante los recorridos al __AST__. Luego encontramos __mip_utils__ donde podemos encontrar 3 clases que son utilizadas durante la conversión de __CIL__ a __mips__ para acceder de manera más sencilla a los strings de los operadores, registros y tipos de datos en __mips__. El archivo __semantic.py__  es uno de los módulos obtenidos durante el desarrollo de las clases prácticas, con algunas modificaciones.  

-visitors: 

​	-__collector.py__: contiene el visitor utilzado solo para registrar los tipos del programa en un objeto context el cual es importado de __semantic.py__. Este visitor solo recorre los nodos que representan declaraciones de clases. 

​	-__builder.py__: primeramente definimos los tipos básicos de __COOL__ así como sus funciones built_in. Además visitamos todos los tipos ya recogidos en el colector para registrar sus métodos y atributos (features). Finalmente nos construimos el grafo de herencia de los tipos para asegurarnos de que no existan ciclos en este.

​	-__checker.py__: revisamos que el programa esté semánticamente correcto. Es decir, una vez nuestro programa es sintácticamente válido corresponde asegurarnos que los tipos de las variables y funciones estén en correspondencia con el contexto en el que se usan. También anotamos a cada nodo su tipo estático para posterior uso durante la generación de código intermedio. Cada nodo existe en un ámbito específico en el cual son visibles variables locales y de ámbitos más externos; cada vez que se visita un nodo se crea un ámbito nuevo en el cual se registren sus variables locales para aquellos casos en los que unas variables solapan a otras  con el mismo lexema pero en ámbitos padres.

​	-__CooltoCill.py__: aca realizamos otro recorrido sobre el __AST__ de __COOL__ con el cual traducimos las instrucciones de alto nivel a instrucciones que simplifiquen el proceso de generar código mips. Nuestro __CIL__ está compuesto por tres secciones: data, donde se registran todas aquellas cadenas de caracteres ya sea especificados por el usuario o por nosotros para lanzar errores en ejecución; type, compuesta por estructuras que agrupan todos los métodos y atributos de cada tipo (features), para luego en la traducción a mips poder organizar de manera más fluida el direccionamiento a estos; por último code, en este se encuentran agrupadas en estructuras el código intermedio generado para cada una de las funciones de los tipos del programa (contructores, built in y definidas por el usuario). Durante el recorrido por los nodos del __AST__ de __COOL__ se genera a la par un nuevo __AST__ esta vez de __CIL__ para luego traducir a __mips__.

​	-__CiltoMips.py__: se utiliza el __AST__ de __CIL__ generado por el recorrido anterior para traducir cada nodo a una secuencia de instrucciones en __mips__ correspondientes al mismo. Primero se visitan los nodos que se encuentran en la sección de data luego la sección de type y por último la sección de code y de esta forma queda organizado el programa en __mips__ añadiendole al final algunas funciones por defecto como 'alocate' para reservar memoria y otras. 

#### Problemas técnicos:

El mayor desafío de implementación que encontramos fue la correcta generación a código intermedio para su posterior traducción a código __mips__ de los nodos __switchcase__ del __AST__ de __COOL__. 

Para ello organizamos las ramas del nodo de mayor a menor, donde las mayores son aquellas cuyo tipo se encuentra a mayor profundidad en el árbol de herencia del programa. Por cada una de estas ramas recorremos el subárbol cuya raiz es el tipo actual de la rama, registrando un salto al label asociado a esta rama. Al recorrer cada uno de estos subárboles, si coincide en algún tipo de este, podemos asegurar que este es el menor tipo  que lo conforma (dado que recorremos las ramas en orden decreciente en profundida).



