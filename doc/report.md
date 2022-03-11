# Proyecto de compilación

## Integrantes

- Enmanuel Verdesia Suárez C-411
- Samuel David Suárez Rodríguez C-412

## Instalación / Ejecución

Para ejecuta el compilador basta con escribir

`bash coolc <filename>.cl` TODO: Finish this

## Arquitectura

Para la implementación del compilador de `COOL` se dividió el proceso de desarrollo en las etapas siguientes:

- Análisis Sintáctico
  - Lexing
  - Parsing
- Análisis Semántico
  - Recolección de tipos (Type collection)
  - Construcción de tipos (Type building)
  - Chequeo de tipos (Type checking)
- Generación de código (Code generation)
  - COOL -> CIL
  - CIL -> MIPS

## Lexing

Para el análisis léxico se utilizó el módulo `ply` de `Python`, el cual permite generar esta parte del proceso de manera automática simplemente definiendo el conjunto de tokens del lenguaje.

...TODO: Más cosas aquí

## Parsing

De igual manera se utilizó `ply` para la fase de parsing debido a que soporta varios tipos de parsers como el parser `LALR(1)` que resuelve de manera eficiente la gramática de `COOL`, esta gramática se definió en base al archivo oficial de `COOL` [cool-manual](./cool-manual.pdf). De esta manera se construye el AST que se usará en las fases de análisis semántico.

...TODO: Más cosas aquí

## Recolección de tipos

Esta fase se encarga de recorrer el AST generado previamente y definir los tipos del lenguaje. Entre estos tipos tenemos los BUILT_IN (Bool, String, Int, IO, Object), así como los tipos definidos en el código por el usuario en las declaraciones de clases. En un recorrido posterior se realiza el chequeo y asignación de padres de tipos, debido a que en el lenguaje las declaraciones de clases se pueden en cualquier orden, por lo que es necesario recolectar los tipos primeramente. En esta fase se resuelven también las excepciones de herencia cíclica.

La lógica para esta fase se implementó en el archivo `collector.py`

## Construcción de tipos

En esta fase se recorre el AST con el objetivo de visitar cada `feature`(método o atributo) de las clases para asignarla a cada tipo y chequear la existencia de una clase `Main` con el método `main`.

La lógica para esta fase se implementó en el archivo `builder.py`

## Chequeo de tipos

Esta fase es la encargada de validar el uso correcto de los tipos definidos en el programa. Determina que las asignaciones de las variables sean a tipos correctos, así como los argumentos de funciones, etc.
...TODO: hablar aqui de esto

La lógica para esta fase se implementó en el archivo `checker.py`

## Generación de código intermedio COOL -> CIL

Para compilar el código en `COOL` a un lenguaje de bajo nivel como `MIPS`, se utilizó un lenguaje intermedio para disminuir la dificultad en la generación de código entre estas dos partes. Para ello definimos un pseudolenguaje (`CIL`) que posee elementos similares al estudiado en clase más algunos agregados y permiten controlar de una manera más sencilla el flujo del programa al generar el código en `MIPS`. Entre estos añadidos tenemos:

- Abort

  `ABORT`: Termina el programa con un mensaje indicando el tipo desde el cual se llamó esta instrucción.

- Errores en tiempo de ejecución:

  `CASE_MATCH_RUNTIME_ERROR`: Devuelve un error en tiempo de ejecución con el mensaje `"RuntimeError: Case statement without a match branch"`. Se usa en las expresiones de tipo case of cuando ninguna rama conforma el resultado de la expresión.

  `EXPR_VOID_RUNTIME_ERROR`: Devuelve un error en tiempo de ejecución con el mensaje: `"RuntimeError: Expression is void"`. Usado para controlar excepciones con expresiones de tipo `void`

- Conforms

  `<var> = CONFORMS <expr> <Type>`: Usada para saber si el resultado de `<expr>` conforma el tipo `<Type>`. Se creó por la necesidad de saber en tiempo de ejecución si el tipo
