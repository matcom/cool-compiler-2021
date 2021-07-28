# Informe sobre el Proyecto de Compilación

## Estudiantes

    - Alejandro Klever Clemente (C-411)
    - Laura Tamayo Blanco (C-411)
    - Miguel Angel Gonzalez Calles (C-411)

### 1. Proceso de parsing y lexing

Para este proceso usamos la biblioteca de python `PyJapt` la cual ha sido desarrollada por este equipo y publicada bajo licencia MIT en GitHub y Pypi.

La documentacion de PyJapt es rica en ejemplos y casos de uso. Puede ser consultada [aqui](https://github.com/alejandroklever/PyJapt).

La gramatica del lenguaje es una gramatica `LALR(1)`, por lo que tenemos unas tablas action y goto bastante pequeñas en comparación con las de una parser `LR(1)`, y por lo tanto mucho mas rápido de construir y menos costoso espacialmente.

Actualmente tanto los test de análisis sintáctico y lexicográficos han sido pasados sin problemas.

### 2. Proceso de análisis semantico

Para esta parte usamos el patrón visitor aprendido durante el curso de 3er año. Por lo cual recibimos el ast obtenido producto del proceso de parsing y pasará por diferentes clases que irán construyendo:

- el contexto: Donde de guardara la información de las clases del programa en COOL.
- el scope: Donde se almacena la información de las atributos, variables y parámetros de cada clase y método.

#### 2.1 Pipeline

Para el proceso de análisis semantico usamos las siguientes clases que usan el patrón visitor para acceder a cada nodo del ast y obtener nueva información en distintos recorridos:

- TypeCollector: Encargada de recolectar los tipos de todas las clases del programa de COOL.
- TypeBuilder: Encargado de recolectar la información de los atributos y metodos de cada clase
- OverriddenMethodChecker: Encargado comprobar que la sobreescritura de metodos es concistente.
- TypeChecker: Encargado del cumplimiento de todas las reglas entre los tipos.

Los tests de semántica están vencidos parcialmente, pues el formato de los mensajes de error aún no es correcto. Estamos trabajando en ello con un primer recorrido que se encargara de asignar a cada nodo del ast la fila y la columna significativa de este de la produccion que generó este nodo.

Por ejemplo, en el caso de los nodos de la instrucción `let declaration-list in expr` la fila y columna significativa será la del keyword `let`.

### 3. Conclusiones

Esperamos proximamente solventar el formato de los errores semanticos siguiendo esta idea. Asi que en resumen, hemos logrado superar la parte de lexing y parsing y estamos cerca de superar los tests de semántica
