# Informe de Complementos de Compilación

## Datos Generales

### Autores

- Yansaro Rodríguez Páez
- Javier Alejandro Valdés González
- Osmany Pérez Rodríguez

## Uso del compilador

## Requisitos para ejecutar el compilador

Para la ejecución es necesario `Python >= 3.7` e instalar los requerimientos listados en _requirements.txt_. Para ello, ejecute el comando:

``` bash
pip install -r requirements.txt
```

Para correr los tests, es necesario tener instalado `make`. Una vez instalado `make` se ejecutan de la siguiente manera:

``` bash
make test
```

Para ello es necesario tener instalado `make`. Para ejecutar un archivo específico se debe correr,desde la raíz del proyecto, el comando:

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
6. Cool a CIL
7. CIL a MIPS

Cada parte del proceso será discutida en detalle durante las siguientes secciones.

## Generalidades del proyecto

A lo largo del proyecto, se aprecia el seguimiento de patrones similares de buenas prácticas de programación para cada uno de los módulos a desarrollar. Veamos algunas generalidades a destacar.

### Manejo de errores

Cada uno de los módulos se encarga de presentar los errores específicos de cada etapa. Estos, a su vez, heredan de una clase `BaseError` declarada en `src/app/shared/errors.py`, la cual es la clase base que presenta las 4 propiedades de un error. Veamos la implementación de `BaseError`:

```python
class BaseError:
    """COOL error"""

    def __init__(self, line: int, column: int, err_type: str, err_message: str):
        self.line = line
        self.column = column
        self.err_type = err_type
        self.err_message = err_message

    def __str__(self) -> str:
        return f"({self.line}, {self.column}) - {self.err_type}: {self.err_message}"

    __repr__ = __str__
```

### Chained (Operador de cascada)

Inspirados en Dart, implementamos una sintaxis similar a lo que sería un `cascade operator` en este lenguaje. Para aprender más sobre los operadores en cascada de Dart [pulse aquí](https://www.educative.io/edpresso/what-is-dart-cascade-notation). Nuestra implementación/adaptación de este operador para python se encuentra en `src/app/shared/cascade.py`, y resultó extremadamente útil/elegante en algunos casos de uso en los que era bastante interesante para hacer una secuencia de métodos sobre un mismo objeto. Veamos en código una de sus aplicaciones a la hora de generar las clases básicas de COOL para el `type_builder`:

``` python
def build_default_classes(self):
        Object = self.context.get_type(OBJECT_TYPE, unpacked=True)
        String = self.context.get_type(STRING_TYPE, unpacked=True)
        Int = self.context.get_type(INT_TYPE, unpacked=True)
        Io = self.context.get_type(IO_TYPE, unpacked=True)
        Bool = self.context.get_type(BOOL_TYPE, unpacked=True)

        String.set_parent(Object)
        Int.set_parent(Object)
        Io.set_parent(Object)
        Bool.set_parent(Object)

        p_Object = self.context.get_type(OBJECT_TYPE)
        p_String = self.context.get_type(STRING_TYPE)
        p_Int = self.context.get_type(INT_TYPE)
        p_Self = self.context.get_type(SELF_TYPE)

        chained(Object)\
            .define_method(ABORT_METHOD_NAME, [], [], p_Object)\
            .define_method(TYPE_NAME_METHOD_NAME, [], [], p_String)\
            .define_method(COPY_METHOD_NAME, [], [], p_Self)

        chained(Io)\
            .define_method(OUT_STRING_METHOD_NAME, ["x"], [p_String], p_Self)\
            .define_method(OUT_INT_METHOD_NAME, ["x"], [p_Int], p_Self)\
            .define_method(IN_STRING_METHOD_NAME, [], [], p_String)\
            .define_method(IN_INT_METHOD_NAME, [], [], p_Int)

        chained(String)\
            .define_method(LENGTH_METHOD_NAME, [], [], p_Int)\
            .define_method(CONCAT_METHOD_NAME, ["s"], [p_String], p_String)\
            .define_method(SUBSTR_METHOD_NAME, ["i", "l"], [
                p_Int, p_Int], p_String)
```

Nótese que se está tomando la misma instancia de un `type` a registrar, y se le esta llamando al método `define_method`, definiendo varios métodos a esa misma instancia, pero con una sintaxis más elegante y expresiva.

### Visitor

También destacar que hacemos uso del patrón visitor para visitar de una manera expresiva los nodos de nuestros ASTs en las distintas fases del pipeline antes descrito. Esta implementación del patrón visitor la podemos encontrar en `src/app/shared/visitor.py`.

## Lexer

En el proceso de tokenización se usó la librería SLY. En esta etapa se ignoran los comentarios de línea así como los espacios en blanco. Para un mejor reporte de errores se dividió la etapa en varios estados:

- MAIN
- block_comment
- strings

En cada uno de estos estados se ejecuta un proceso de tokenización especializado. En el caso de los `block_comment` se maneja el caso de comentarios identados, y en string se manejan errores específicos como "No debe existir el carácter NULL" o "String no terminado".

### Detalles sobre la implementación (Lexer)

Se usó una clase `BaseLexer` donde se implementa la forma de manejar un error no esperado, así como el método `_leave_context_` usado para regresar al estado de lexer anterior.

_sly_ no brinda soporte para llevar un seguimiento de la línea actual, por lo que en cada cambio de línea(`\n`), aumentamos el numero de línea correspondiente y lo asociamos al token.

### Gramática de Cool

La gramática utilizada es libre de contexto y de recursión extrema izquierda. Esto trae consigo que se presenten problemas de ambigüedad que son resueltos con la definición de reglas de precedencia en la implementación del parser. (El el caso de SLY esto se resuelve ordenando los valores en la propiedad `precedence` de la clase `Parser`)

## Parsing

El parser se encarga de construir el AST haciendo uso de los nodos definidos en (parser/ast). Los métodos del parser están precedidos por un decorador que especifica que producción va a analizar el método haciendo uso de la librería SLY, y este a su vez devuelve el resultado de parsear el nodo del AST correspondiente.

### Detalles de la implementación (Parsing)

Cada uno de los nodos de nuestro AST, se encuentran separados en diferentes archivos para un mayor desacoplamiento y entendimiento del código.

#### Base

En `base.py`, se declara inicialmente el tipo base de la jerarquía de clases de nuestro AST, llamado `AstNode`.

```python
class AstNode:
    '''Base clase for AST parser'''

    def __init__(self, lineno, columnno):
        self.lineno = lineno
        self.columnno = columnno

```

Este nodo contiene la información básica de un nodo del AST para el proceso de parsing. Acto seguido, se declaran otros nodos escogidos como "bases". Todos estos tipos de objetos, sirven de base en nuestra jerarquía de clases para la herencia. Veamos nuestra jerarquía de clases:

- AstNode
  - ProgramNode
  - ClassNode
  - FeatureNode
    - AttrDeclNode
    - MethodDeclNode
  - ExprNode
    - AssignNode
    - StaticDispatchNode
    - DispatchNode
    - IfThenElseNode
    - WhileNode
    - BlockNode
    - LetInNode
    - CaseNode
    - NewNode
    - ParenthNode
    - AtomNode
      - IntNode
      - StringNode
      - BoolNode
      - VarNode
    - UnaryExprNode
      - IsVoidNode
      - NotNode
      - TildeNode
    - BinaryExprNode
      - ArithmeticNode
        - PlusNode
        - MinusNode
        - MultNode
        - DivNode
      - ComparisonNode
        - LeqNode
        - EqNode
        - LeNode
  - LetDeclNode
  - CaseBranchNode

Siguiendo un paradigma de programación orientada a objetos, cada nodo del AST presenta un método estático que funciona como [factory constructor](https://es.wikipedia.org/wiki/Factory_Method_(patr%C3%B3n_de_dise%C3%B1o)), el cual permite delegar la construcción del nodo a sí mismo. Para ello hacemos uso del decorador `@staticmethod`, declarando un método parse para cada uno de los métodos. Decidimos no crear este método en nuestra clase base, y hacer override de este en cada una de las subclases, debido a que no todos los nodos recibían los mismos argumentos, así que que la solución basada en herencia con sobrescritura de los métodos no nos pareció la más elegante.

## Análisis Semántico

### Recolección de tipos

Para la recolección de tipos, al igual que para la mayoría de las etapas del proyecto se utiliza el patrón `visitor`. Aquí se realiza un recorrido por el AST generado en la etapa de parsing, definiendo en el contexto los tipos encontrados y chequeando si ocurre alguno de los siguentes errores:

**Errores detectados**:

- Herencia cíclica
- Herencia no válida(no se deben redefinir `Int`, `Bool` o `String`)

### Construcción de tipos

En esta etapa se verifica primeramente que el programa ofrecido sea válido, esto supone que tenga una clase principal `Main` con un método `main` sin argumentos. También en el recorrido por el AST se incluyen en el contexto los métodos y atributos declarados en cada clase.

**Errores detectados**:

- Redefinición en un hijo sin conservar la cantidad de argumentos o tipo de retorno
- Redefinición de atributos
- Uso de tipos no definidos
- No definición de la clase `Main` o su método `main`
- Incorrecta definición del método `main`

### Chequeo de tipos

El chequeo de tipos se dividió en dos etapas. Primeramente se realiza un recorrido sin profundidad, infiriendo los tipos declarados conforme su anotación, llamando a este recorrido `SoftInferrer`. Luego se realiza otro recorrido con la información de los tipos inferidos en el recorrido anterior.

En este ultimo recorrido `DeepInferrer` se infiere el tipo más especifico y se verifica que este tipo se conforme con el tipo de la anotación, aquí se incluyen los chequeos para los `case`, verificar que los operadores aritméticos solo puedan ser utilizados con `Int`, etc. Es necesario destacar aquí el uso de dos tipos inferidos para cada nodo, un `inferred_type` y un `execution_inferred_type`. Este último se usa por la siguiente razón:

Asumamos que tenemos una clase `A` en la que se define un método `bar` que devuelve `self` y `foo` devolviendo `true`. y que también tenemos una clase hija `B` que sobrescribe `bar` devolviendo `self` pero anotado como `A` y `foo` retornando `false` . En el proceso de chequeo de tipos `B.test()` tiene q devolver `A` ya que así esta anotado, pero es necesario saber que el tipo real es `B` en el proceso de ejecución. Pues `B.bar().foo()` debería retornar `false` como esta definido en `self`(`B`)

**Errores detectados**:

- Incompatibilidad de tipos
- Uso de variables, tipos y métodos no definidos
- mal usos del `case`
  
### Detalles de la implementación (Semantics)

Cabe destacar en este recorrido semántico, se genera un nuevo AST dado el AST que genera el proceso anterior en el pipeline (Parser). Sobre este nuevo AST, se sigue la misma idea de POO descrita en el proceso de parsing. Cada nodo se hace resposable de chequear su inferencia, por lo que en cada nodo podremos ver 2 métodos estáticos o factory constructor: `soft_infer` y `deep_infer`, usados evidentemente, en cada uno de los procesos anteriormente descritos respectivamente.

También se desarrolló una jerarquía de clases para los nodos de este nuevo AST, homóloga a la del proceso de parsing previamente descrito.

## COOL a CIL

CIL es un lenguaje intermedio 3-address pero a su vez orientado a objetos, esto nos facilita el mapeo de la mayoría de las expresiones COOL a nodos de un AST de CIL. Se toma como caso interesante la instrucción `case`, en la cual se ordenan las ramas con un orden topológico, donde `a` tiene una arista hacia `b` si `a` se conforma con `b`. Luego la ejecución se realiza en este orden. Luego por cada tipo en el programa verificamos si este se conforma con el tipo de la instrucción `case` y no ha sido usado anteriormente. Aquí se manejan errores lanzados en ejecución como excepciones aritméticas o índices fuera de rango. Las principales secciones del código CIL, en este caso representado mediante el AST, son:

- `.TYPE`: se guarda lo que en equivalencia se puede llamar las clases, aunque no hay ningún inicializado por defecto y los métodos lo que contienen es como una referencia a la definición real de la función que se implementará en `.CODE`
- `.DATA`: se declaran las variables que representan valores constantes en la ejecución.
- `.CODE`: implementación de las funciones que son referenciadas en las definiciones de clases, con la particularidad que la primera es la que representa el inicio del programa; lo que comúnmente es el método main.

**Errores detectados**:

- Dispatch desde void
- Index out of range
- Ejecución de un _case_ sin que ocurra algún emparejamiento con alguna rama.
- División por cero

## CIL a MIPS

A la hora de traducir de código CIL a MIPS es necesario apoyarse del patrón visitor nuevamente que tiene como punto de partida el AST de CIL que genera el paso anterior. El código MIPS tiene dos secciones que lo divide: .DATA (se crean referencias a objetos con un valor predeterminado o a otras direcciones de memoria) y .TEXT( se define como tal la lógica del código con las instrucciones que esto conlleva). Después se realiza otro visitor sencillo donde se traduce el AST de MIPS a código en sí, cada instrucción recibe una representación en un string y esto posteriormente en un archivo que finalmente será ejecutado en SPIM.

### CIL Type en memoria

Al no soportar MIPS instrucciones orientadas a objetos es necesario elaborar una variante para la representación de un tipo de CIL, necesitamos para esto el nombre del tipo. Para almacenar los datos del objeto se utilizo el patrón _Prototype_, algo parecido a lo que realiza JavaScript con sus objetos. Para cada tipo existe un prototype el cual es copiado a la dirección del objeto creado en cada creación almacenando también en el prototype los valores por defecto de cada objeto. Luego para los métodos del objeto se almacenan sus direcciones en lo que es conocido como `tabla dispatch`:

En conclusión, los prototypes se usan como valor por default de un objeto de un tipo especifico a la hora de su creación, todo tipo tiene un prototype asignado.

### Objetos en MIPS

La representación de un objeto en CIL una vez que se traduce a MIPS seria la siguiente:

- Type(`1 word`): es un mapeo a un número entero que mapea a un tipo. La lista `shells_table` permite acceder al espacio de memoria donde está almacenado el tipo a través de ese número entero que hace función de índice.
- Size (`1 word`): tamaño en words del tipo. La suma de la cantidad de atributos + 3 (estos campos que se están explicando en este momento).
- DispatchTable (`1 word`): Dirección a la tabla dispatch del objeto. Esta contiene las direcciones de las funciones del tipo como tal.
- Attributes (`n words`): Direcciones de los atributos en memoria, estos se almacenan con el nombre de la clase y el nombre del atributo.

Un objeto cuya dirección inicial en memoria sea x queda de la siguiente forma:

| Dirección x | Dirección x + 4 | Dirección x + 8   | Dirección x + 8 | ... | Dirección x + (a + 2 ) \* 4 |
| ----------- | --------------- | ----------------- | --------------- | --- | --------------------------- |
| Tipo        | Tamaño          | Tabla de dispatch | Atributo $0$    | ... | Atributo $a$                |

**Llamado dinámico a una función**

Para cada tipo, se guardan sus métodos en una lista llamada type\_\<tipo>\_dispatch. Esta tiene la siguiente estructura, partiendo de que su inicio es en la dirección x.

| Dirección x | Dirección x + 4 | Dirección x + 8 | ... | Dirección x + (m-1) \* 4 |
| ----------- | --------------- | --------------- | --- | ------------------------ |
| Método 0    | Método 1        | Método 2        | ... | Método m-1               |

Por cada uno de los tipos se crea una de estas tablas, que contiene (cantidad de métodos) \* words espacio de memoria asignado. Cada elemento entonces apunta a la etiqueta donde se define la función.

Dichas funciones en la lista están en el orden en el que fueron definidos, que si heredan por defecto vienen con los métodos de los ancestros en su inicio a través del procesamiento para generar el código CIL.

Una vez que se tiene el tipo al que se le realiza el llamado, dada la estructura del objeto es fácil saber a que dispatch table se requiere hacer la visita. Con el apoyo de un índice se accede entonces al método apropiado.

| Dirección $x$  | Dirección $x + 4$ | Dirección $x + 8$ | ... | Dirección $x + (n-1) * 4$ |
| -------------- | ----------------- | ----------------- | --- | ------------------------- |
| _dispatch_ $0$ | _dispatch_ $1$    | _dispatch_ $2$    | ... | _dispatch_ $n - 1$        |

Donde $n$ es la cantidad de tipos, los nombres de las tablas dispatch están representadas con el nombre del tipo pero aquí para propósitos demostrativos se le asigna un número entero que es el mismo que se muestra en la estructura de un objeto cuando se habla del campo `Tipo`.

Y entonces para el llamado al método deseado se hace un proceso análogo de indexar con un índice conocido mediante el procesamiento y las variables del código que almacenan dicha información. Luego, se obtiene la dirección al método y se hace un jump a dicha etiqueta.

## Estructura del proyecto

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
