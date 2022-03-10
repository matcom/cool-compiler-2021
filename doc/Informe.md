# Informe de Complementos de Compilación
## Datos Generales
### Autores
- Yansaro Rodríguez Páez
- Javier Alejandro Valdés González
- Osmany Pérez Rodríguez

## Uso del compilador

## Requisitos para ejecutar el compilador
Para la ejecución es necesario `Python >= 3.7` e instalar los requerimientos listados en *requirements.txt*. Esto se hace de manera fácil con la instrucción *pip install -r requirements.txt*. 

Para correr los tests se debe ejecutar `make test`. Para esto es necesario tener instalado `make`. Para ejecutar un archivo especifico se debe correr

```bash
python3 -m app $INPUT_FILE
```


## Pipeline
El programa cuenta con las siguientes etapas:

1. Lexer
2. Parsing
3. Recolección de tipos
4. Construcción de tipos
5. Chequeo de tipos
7. Cool a CIL
8. CIL a MIPS

Cada parte del proceso será discutida en detalle durante las siguientes secciones.

## Lexer

En el proceso de tokenizacion se uso la libreria SLY. En esta etapa se ignoran los comentarios de linea asi como los espacios en blanco. Para un mejor reporte de errores se dividio la etapa en varios estados: 

   - MAIN
   - block_comment
   - strings

En cada uno de estos estados se ejecuta un proceso de tokenización especializado. En el caso de los `block_comment` se maneja el caso de comentarios identados, y en string se manejan errores especificos como "No debe existir el caracter NULL" o "String no terminado".

### Gramática de Cool

La gramática utilizada es libre de contexto y de recursión extrema izquierda. Esto trae consigo que se presenten problemas de ambigüedad que son resueltos con la definición de reglas de precedencia en la implementación del parser. (El el caso de SLY esto se resuelve ordenando los valores en la propiedad `precedence` de la clase `Parser`)

## Parsing
El parser se encarga de contruir el AST haciendo uso de los nodos definidos en (parser/ast). Los metodos del parser están precedidos por un decorador que especifica que producción va a analizar el método, y este a su vez devuelve el resultado de parsear el nodo del AST correspondiente.



## Análisis Semántico

### Recolección de tipos 

Para la recoleccion de tipos, al igual que para la mayoria de las etapas del proyecto se utiliza el patron `visitor`. Aqui se realiza un recorrido por el AST generado en la etapa de parsing, definiendo en el contexto los tipos encontrados y chequeando si ocurre alguno de los siguentes errores:

**Errores detectados**:
- Herencia cíclica
- Herencia no valida(no se deben redefinir  `Int`, `Bool` o `String`)



### Construcción de tipos

En esta etapa se verifica primeramente que el programa ofrecido sea valido, esto supone que tenga una clase principal `Main` con un metodo `main` sin argumentos. Tambien en el recorrido por el AST se incluyen en el contexto los metodos y atributos declarados en cada clase.

**Errores detectados**:

- Redefinición en un hijo sin conservar la cantidad de argumentos o tipo de retorno
- Redefinición de atributos
- Uso de tipos no definidos 
- No definición de la clase `Main` o su método `main`
- Incorrecta definición del método `main`

### Chequeo de tipos

El chequeo de tipos se dividió en dos etapas. Primeramente se realiza un recorrido sin profundidad, infiriendo los tipos declarados conforme su anotación, llamando a este recorrido `ShahahallowInferrer` o con su nombre mas conocido `LadyGagaInferrer` (😂). Luego se realiza otro recorrido con la información de los tipos inferidos en el recorrido anterior. 

En este ultimo recorrido `DeepInferer` también conocido como `BradleyCooperInferer` se infiere el tipo mas especifico y se verifica q este tipo se conforme con el tipo de la anotación, aquí se incluyen los chequeos para los `case`, verificar que los operadores aritméticos solo puedan ser utilizados con `Int`,  etc. Es necesario destacar aquí el uso de dos tipos inferidos para cada nodo, un `inferred_type` y un `execution_inferred_type`. Esto ultimo se usa por la siguiente razón:

​	Asumamos que tenemos una clase `A` en la que se define un método `bar` que devuelve `self` y `foo` devolviendo `true`.  y que también tenemos una clase hija `B` que sobrescribe `bar` devolviendo `self` pero anotado como `A` y `foo` retornando `false` . En el proceso de chequeo de tipos `B.test()` tiene q devolver `A` ya que así esta anotado, pero es necesario saber que el tipo real es `B` en el proceso de ejecución. Pues `B.bar().foo()` debería retornar `false` como esta definido en `self`(`B`) 

**Errores detectados**:

- Incompatibilidad de tipos
- Uso de variables, tipos y métodos no definidos
- mal usos del `case` 



## COOL a CIL

CIL es un lenguaje intermedio 3-address pero a su vez orientado a objetos, esto nos facilita el mapeo de la mayoría de las expresiones COOL a nodos de un AST de CIL. Se toma como caso interesante la instrucción `case`, en la cual se ordenan las ramas con un orden topológico, donde `a` tiene una arista hacia `b` si `a` se conforma con `b`. Luego la ejecución se realiza en este orden. Luego por cada tipo en el programa verificamos si este se conforma con el tipo de la instrucción `case` y no ha sido usado anteriormente. Aquí se manejan errores lanzados en ejecución como excepciones aritméticas o índices fuera de rango. Las principales secciones del código CIL, en este caso representado mediante el AST, son:

- `.TYPE`: se guarda lo que en equivalencia se puede llamar las clases, aunque no hay ningún inicializado por defecto y los métodos lo que contienen es como una referencia a la definición real de la función que se implementará en `.CODE`
- `.DATA`: se declaran las variables que representan valores constantes en la ejecución.
- `.CODE`: implementación de las funciones que son referenciadas en las definiciones de clases, con la particularidad que la primera es la que representa el inicio del programa; lo que comunmente es el método main.

**Errores detectados**:

- Dispatch desde void
- Index out of range
- Ejecución de un *case* sin que ocurra algún emparejamiento con alguna rama.
- División por cero

## CIL a MIPS


A la hora de traducir de código CIL a MIPS es necesario apoyarse del patrón visitor nuevamente que tiene como punto de partida el AST de CIL que genera el paso anterior. El código MIPS tiene dos secciones que lo divide: .DATA (se crean referencias a objetos con un valor predeterminado o a otras direcciones de memoria) y .TEXT( se define como tal la lógica del código con las instrucciones que esto conlleva). Después se realiza otro visitor sencillo donde se traduce el AST de MIPS a código en sí, cada intrucción recibe una representación en un string y esto posteriormente en un archivo que finalmente será ejecutado en SPIM. 
### CIL Type en memoria.

Al no soportar MIPS instrucciones orientadas a objetos es necesario elaborar una variante para la representación de un tipo de CIL, necesitamos para esto el nombre del tipo. Para almacenar los datos del objeto se utilizo el patrón *Prototype*, algo parecido a lo que realiza JavaScript con sus objetos. Para cada tipo existe un prototype el cual es copiado a la dirección del objeto creado en cada creación almacenando también en el prototype los valores por defecto de cada objeto. Luego para los métodos del objeto se almacenan sus direcciones en lo que es conocido como `tabla dispatch`:

En conclusión, los prototypes se usan como valor por default de un objeto de un tipo especifico a la hora de su creación, todo tipo tiene un prototype asignado.

### Objetos en MIPS.
La representación de un objeto en CIL una vez que se traduce a MIPS seria la siguiente:

 - Type(`1 word`): es un mapeo a un número entero que mapea a un tipo. La lista `shells_table` permite acceder al espacio de memoria donde está almacenado el tipo a través de ese número entero que hace función de índice. 
 - Size (`1 word`): tamaño en words del tipo. La suma de la cantidad de atributos + 3 (estos campos que se están explicando en este momento).
 - DispatchTable (`1 word`): Dirección a la tabla dispatch del objeto. Esta contiene las direcciones de las funciones del tipo como tal.
 - Attributes (`n words`):  Direcciones de los atributos en memoria, estos se almacenan con el nombre de la clase y el nombre del atributo.

Un objeto cuya dirección inicial en memoria sea x queda de la siguiente forma:

| Dirección x | Dirección x + 4 | Dirección x + 8      | Dirección x + 8      |... | Dirección x + (a + 2 ) * 4 |
| ----------- | --------------- | ---------------------| ---------------------|--- | -------------------------- |
| Tipo        | Tamaño          | Tabla de dispatch    | Atributo $0$         |... | Atributo $a$               |


**Llamado dinámico a una función**

Para cada tipo, se guardan sus métodos en una lista llamada type_\<tipo>_dispatch. Esta tiene la siguiente estructura, partiendo de que su inicio es en la dirección x.

| Dirección x | Dirección x + 4 | Dirección x  + 8 | ... | Dirección x + (m-1) * 4 |
| ----------- | --------------- | ---------------- | --- | ----------------------- |
| Método 0    | Método 1        | Método 2         | ... | Método m-1              |

Por cada uno de los tipos se crea una de estas tablas, que contiene (cantidad de métodos) * words espacio de memoria asignado. Cada elemento entonces apunta a la eiqueta donde se define la función.

Dichas funciones  en la lista están en el orden en el que fueron definidos, que si heredan por defecto vienen con los métodos de los ancestros en su inicio a través del procesamiento para generar el código CIL.

Una vez que se tiene el tipo al que se le realiza el llamado, dada la estructura del objeto es fácil saber a que dispatch table se requiere hacer la visita. Con el apoyo de un índice se accede entonces al método apropiado.

| Dirección $x$  | Dirección $x + 4$ | Dirección $x + 8$ | ... | Dirección $x + (n-1) * 4$ |
| -------------- | ----------------- | ----------------- | --- | ------------------------- |
| _dispatch_ $0$ | _dispatch_ $1$    | _dispatch_ $2$    | ... | _dispatch_ $n - 1$        |

Donde $n$ es la cantidad de tipos, los nombres de las tablas dispactch están representadas con el nombre del tipo pero aquí para propósitos demostrativos se le asigna un número entero que es el mismo que se muestra en la estructura de un objeto cuando se habla del campo `Tipo`.

Y entonces para el llamado al método deseado se hace un proceso análogo de indexar con un índice conocido mediante el procesamiento y las variables del código que almacenan dicha información. Luego, se obtiene la dirección al método y se hace un jump a dicha etiqueta.


## Estructura
```bash 
├── app
│   ├── cil
│   │   ├── cil.py
│   │   └── cool_to_cil.py
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── lexer
│   │   ├── base.py
│   │   ├── block_comments.py
│   │   ├── errors.py
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── strings.py
│   ├── __main__.py
│   ├── mips
│   │   ├── cil_to_mips.py
│   │   ├── mips.py
│   │   └── utils
│   │       ├── boolean_operations.py
│   │       ├── __init__.py
│   │       ├── IO_operations.py
│   │       ├── memory_operations.py
│   │       └── string_operations.py
│   ├── parser
│   │   ├── ast
│   │   │   ├── arithmetic.py
│   │   │   ├── atomics.py
│   │   │   ├── base.py
│   │   │   ├── comparison.py
│   │   │   ├── expressions.py
│   │   │   ├── features.py
│   │   │   ├── __init__.py
│   │   │   └── unaries.py
│   │   ├── errors.py
│   │   ├── __init__.py
│   │   └── parser.py
│   ├── semantics
│   │   ├── ast
│   │   │   ├── arithmetics.py
│   │   │   ├── atomics.py
│   │   │   ├── base.py
│   │   │   ├── comparison.py
│   │   │   ├── declarations.py
│   │   │   ├── expressions.py
│   │   │   ├── __init__.py
│   │   │   └── unaries.py
│   │   ├── constants.py
│   │   ├── inference
│   │   │   ├── deep_inferrer.py
│   │   │   ├── __init__.py
│   │   │   └── soft_inferencer.py
│   │   ├── __init__.py
│   │   ├── tools
│   │   │   ├── context.py
│   │   │   ├── errors.py
│   │   │   ├── __init__.py
│   │   │   ├── scope.py
│   │   │   └── type.py
│   │   ├── type_builder.py
│   │   └── type_collector.py
│   └── shared
│       ├── cascade.py
│       ├── errors.py
│       └── visitor.py
├── ast.json
├── coolc.sh
├── makefile
├── parser.log
├── parser.out
└── Readme.md
```

En shared se encuentran los errores base y la implementación del patrón *visitor* usando decoradores
