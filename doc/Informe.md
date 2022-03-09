# Informe de Complementos de Compilación
## Datos Generales
### Autores
- Yansaro Rodríguez Páez
- Javier Alejandro Valdés González
- Osmany Pérez Rodríguez

## Uso del compilador




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

CIL es un lenguaje intermedio 3-address pero a su vez orientado a objetos, esto nos facilita el mapeo de la mayoría de las expresiones COOL a nodos de un AST de CIL. Se toma como caso interesante la instrucción `case`, en la cual se ordenan las ramas con un orden topológico, donde `a` tiene una arista hacia `b` si `a` se conforma con `b`. Luego la ejecución se realiza en este orden. Luego por cada tipo en el programa verificamos si este se conforma con el tipo de la instrucción `case` y no ha sido usado anteriormente. Aquí se manejan errores lanzados en ejecución como excepciones aritméticas o índices fuera de rango.

**Errores detectados**:

- Dispatch desde void
- Index out of range
- Ejecución de un *case* sin que ocurra algún emparejamiento con alguna rama.
- División por cero

## CIL a MIPS
### CIL Type en memoria.

Al no soportar MIPS instrucciones orientadas a objetos es necesario elaborar una variante para la representación de un tipo de CIL, necesitamos para esto el nombre del tipo. Para almacenar los datos del objeto se utilizo el patrón *Prototype*, algo parecido a lo que realiza JavaScript con sus objetos. Para cada tipo existe un prototype el cual es copiado a la dirección del objeto creado en cada creación almacenando también en el prototype los valores por defecto de cada objeto. Luego para los métodos del objeto se almacenan sus direcciones en lo que es conocido como `tabla dispatch`:

En conclusión, los prototypes se usan como valor por default de un objeto de un tipo especifico a la hora de su creación, todo tipo tiene un prototype asignado.

### Llevando objetos específicos a MIPS.
La representación en memoria de un objeto en CIL seria la siguiente:

 - Prototype (`1 word`): indica el prototype del objeto.
 - Size (`1 word`): tamaño en words.
 - DispatchTable (`1 word`): Dirección a la tabla dispatch del objeto.
 - Attributes (`n words`):  Direcciones de los atributos en memoria, estos se almacenan con el nombre de la clase y el nombre del atributo.
 - Mark (`1 word`): Tiene la dirección de este espacio de memoria para indicar q el objeto lo usa.

## Requisitos para ejecutar el compilador
Para la ejecución es necesario `Python >= 3.7` e instalar los requerimientos listados en *requirements.txt*. Esto se hace de manera fácil con la instrucción *pip install -r requirements.txt*. 

Para correr los tests se debe ejecutar `make test`. Para esto es necesario tener instalado `make`. Para ejecutar un archivo especifico se debe correr

```bash
python3 -m app $INPUT_FILE
```

## Estructura
- **app**
  - **lexer**
  - **parser**
  - **cil**
  - **mips**
  - **shared**
  - **semantic**

En shared se encuentran los errores base y la implementación del patrón *visitor* usando decoradores
