# Cool Compiler Project

## Integrantes

- Thalía Blanco Figueras
- Nadia González Fernández
- José Alejandro Labourdette-Lartigue Soto

## Introducción

El proyecto implementa un compilador capaz de interpretar el lenguaje COOL 
"The Classroom Object-Oriented Language". La solución está desarrollada en python.


## Lexer y Parser
Para el desarrollo del lexer y el parser se utilizó la herramienta de parsing **PLY**.
Esta es una implementación en python de lex/yacc.

### Gramática
La gramática usada es libre de contexto y de recursión extrema izquierda. Debido a la forma
en la que esta es definida, no presenta problemas de ambigüedad

```
program : class_list

class_list : class_def
        | class_def class_list
        
class_def : CLASS TYPE_ID LBRACE feature_list RBRACE SEMICOLON
          | CLASS TYPE_ID INHERITS TYPE_ID LBRACE feature_list RBRACE SEMICOLON

feature_list : attrs_def SEMICOLON feature_list
             | meth_def SEMICOLON feature_list
             | empty
                 
attrs_def : attr_def
          | attr_def COMMA attrs_def
          
attr_def : OBJECT_ID COLON type
         | OBJECT_ID COLON type ASSIGN expr
         
meth_def : OBJECT_ID LPAREN param_list RPAREN COLON type LBRACE expr RBRACE

param_list : param other_param
           | empty
           
param : OBJECT_ID COLON type

other_param : COMMA param other_param
            | empty
            
expr : comparer LT open_expr_lvl1
     | comparer LTEQ open_expr_lvl1
     | comparer EQ open_expr_lvl1
     | open_expr_lvl1
     | comparer
     
open_expr_lvl1 : arith PLUS open_expr_lvl2
               | arith MINUS open_expr_lvl2
               | open_expr_lvl2
               
open_expr_lvl2 : term MULT open_expr_lvl3
               | term DIV open_expr_lvl3
               | open_expr_lvl3
               
open_expr_lvl3 : ISVOID open_expr_lvl3
               | INT_COMP open_expr_lvl3
               | open_expr
               
open_expr : LET let_var_list IN expr
          | OBJECT_ID ASSIGN expr
          | NOT expr
               
comparer : comparer LT arith
         | comparer LTEQ arith
         | comparer EQ arith
         | arith
         
arith : arith PLUS term
      | arith MINUS term
      | term
      
term : term MULT factor
     | term DIV factor
     | factor
     
factor : ISVOID factor
       | INT_COMP factor
       | atom
       
atom : INTEGER
     | OBJECT_ID
     | STRING
     | BOOL
     | LPAREN expr RPAREN
     | NEW TYPE_ID
     | IF expr THEN expr ELSE expr FI
     | WHILE expr LOOP expr POOL
     | LBRACE expr_list RBRACE
     | CASE expr OF branch_list ESAC
     | func_call
      
expr_list : expr SEMICOLON
          | expr SEMICOLON expr_list
          
let_var_list : OBJECT_ID COLON type
             | OBJECT_ID COLON type ASSIGN expr
             | OBJECT_ID COLON type COMMA let_var_list
             | OBJECT_ID COLON type ASSIGN expr COMMA let_var_list
             
branch_list : OBJECT_ID COLON type ACTION expr SEMICOLON
            | OBJECT_ID COLON type ACTION expr SEMICOLON branch_list
            
func_call : atom DOT OBJECT_ID LPAREN arg_list RPAREN
          | OBJECT_ID LPAREN arg_list RPAREN
          | atom AT TYPE_ID DOT OBJECT_ID LPAREN arg_list RPAREN
          
arg_list : expr other_arg
         | empty
         
other_arg : COMMA expr other_arg
          | empty
          
type : TYPE_ID
        | SELF_TYPE
        
empty :
```
Las expresiones del lenguaje pueden separarse en dos grupos:

- Las que se conoce donde empiezan y terminan. Estas tienen un terminal específico 
  para iniciarlas y otro para finalizarlas, y esos terminales siempre van a ser los mismos. 
  Por ejemplo las condiciones empiezan con `IF` y termina con `FI`, los ciclos con `WHILE` y `POOL`. 

- Las que no cumplen la condición anterior. Estas empiezan o terminan con no terminales. 
  En este grupo se presentan problemas de precedencia o conflictos y la gramática tiene 
  que encontrar una forma de solucionarlos. 
  
La definición del lenguaje deja claro que las expresiones **let**, **assign** y **not** 
consumen todos los tokens que le siguen. Luego, con un nivel de precedencia mayor, están las expresiones 
de comparación y después las aritméticas. Para disminuir al mínimo la precedencia de las expresiones let, assign y not se utilizan los no 
terminales `open_expr_lvlx`. Una expresión intenta encontrar todas las comparaciones o expresiones 
aritméticas antes del terminal que marca el comienzo de la expresión let, assign o not. Luego,
toda la cadena de tokens que sigue se sabe que pertenece al cuerpo de estas expresiones 
(que es también una expresión).

Para garantizar la precedencia correcta en las expresiones de comparación y aritméticas se
usa la distinción entre comparador, arith, término, factor y átomo. Donde un átomo se puede
ver sin problemas como alguna de estas expresiones donde su inicio y fin están bien definidos.

## Lexer
En la implementación del lexer se declaran los tokens, que definien todos los posibles tokens 
que el compilador recibirá. Esta lista también se utiliza en el parser. 
Estos tokens se definen con la expresión regular compatible con el módulo **re** de Python

**Ejemplo:**
```python
tokens = ['INTEGER', 'PLUS', 'MINUS', 'MULT', 'DIV']

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t
```

En el lexer se define el número de línea de cada token.

```python
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
```

## Parser

En la implementación del parser se utiliza `ast_hierarchy.py`. En este se definen los
nodos del árbol que se construirá en el parser. Las reglas de gramática mostradas 
anteriormente se definen en python utilizando la biblioteca `ply`:

```python
def p_class_list(p):
    """
    class_list : class_def
               | class_def class_list
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]
```

Los errores de esta fase son manejados por ply.yacc:

```python
def p_error(p):
    if p is None:
        line_no = find_last_line(input_text)
        errors.append('(%s, 0) - SyntacticError: ERROR at or near EOF' % line_no)
    else:
        col_no = find_column(input_text, p)
        errors.append(('(%s, %s) - SyntacticError: ERROR at or near "%s"'.format(p) % (p.lineno, col_no, p.value)))
```

Los nodos del ast que se crean tienen en común los dos primeros argumentos: 
la fila y la columna en la que se encuentran. Por esta razón existen estructuras que podían 
ser representadas fácilmente como una tupla de datos, sin embargo tenía más sentido 
hacerlas nodos propios capaces de almacenar la línea en la que se encuentran. Un ejemplo
es el caso de la expresión **Case**: cada elemento de la `branch_list` es un nodo. Sucede
muy a menudo que estos son escritos en otras líneas del programa, y de ocurrir algún error en ellos
se informaría que se encuentra en la línea en la que se empezó a definir la expresión del Case.


## Análisis Semántico

Para el análisis semántico seguimos un patrón visitor. Se hacen 3 recorridos por el ast en esta fase:

- [Type Collector](/src/type_collector.py) 
- [Type Builder](/src/type_builder.py)
- [Type Checker](/src/type_checker.py)

En el `TypeCollector` se hace un primer recorrido por el AST recolectando todos los tipos. 
También se añaden los tipos predefinidos por el lenguaje COOL.

En el `TypeBuilder` se analizan los cuerpos de cada clase. Por cada atributo o función visitado
se crea ese feature en el tipo definido en el contexto. Adicionalmente se comprueba que los tipos
utilizados para esos atributos, los tipos de retorno y de los parámetros de las funciones sean 
tipos declarados ya en el contexto.

En el `TypeChecker` se hace un análisis semántico a profundidad. Se visitan todos los
nodos del ast y se comprueba que se correspondan los tipos esperados y
que los llamados a funciones sean con el número y tipo de argumentos requeridos. 
Además se comprueba que se usen variables ya definidas en los **scopes**, 
y es que precisamente en este recorrido es en el que se crean los scopes de las 
variables del programa. Para resolver los problemas de herencia de atributos se asigna
a la propiedad parent del scope que crea la clase que hereda, el scope creado por la 
clase heredada. Esta técnica es usada cada vez que interesa crear scopes específicos para ciertas
secciones.

## Generador de Código

El objetivo de esta etapa es bajar de **COOL**, que es un lenguaje de alto nivel que usa el concepto de herencia y polimorfismo,
hasta código **MIPS**, que es de bajo nivel y donde está plano todo ese código. Como esta traducción del programa no es
inmediata utilizamos un lenguaje intermedio que es **CIL** que nos facilita este cambio. Entonces se realizan dos
traducciones: de **COOL** a **CIL**, y de **CIL** a **MIPS**

### Cool a CIL
Para esta traducción se realiza un recorrido por el ast de COOL con un patrón visitor y toman las acciones pertinentes
dependiendo del tipo de nodo que se analiza. Este recorrido devuelve una estructura que contiene, en nodos de CIL, 
el programa. Atendiendo a los principios de CIL existen 3 secciones para un programa escrito en ese lenguaje:
la sección `Types` donde se define la estructura que tienen los tipos en COOL (entiéndase por esto los atributos
o funciones que se definen en él, o en clases ancestras) y estos atributos tienen un orden específico; la sección
`Data` donde están definidas las constantes del programa, en este caso tendremos todos los strings que se usan en él; 
y la sección `Code` donde están definidas todas las funciones del programa, siendo la primera de ellas la que se usa 
como función de inicio.

Para hacer instancias de los tipos de Cool se crea una función especial en CIL, que no es más que una especie de 
constructor, que inicializa cada uno de los atributos de esa clase.

Durante este proceso de traducción se tienen variables de instancias de la clase encargada de implementar el patrón
visitor (COOLToCILVisitor). Estas variables son **dottypes**, **dotdata** y **dotcode** que continen los nodos
correspondientes a estas secciones de las que hablamos recién; **current_type** y **current_method** que denotan el 
tipo y el método que se analizan actualmente en el ast de Cool; **current_function** que es el nodo función que se está 
creando actualmente de CIL.


### CIL a MIPS

Para esta traducción se recorrerá ahora el ast de CIL generado en el proceso anterior. El primer problema a solucionar
es como representar los objetos en memoria. Como convenio tendremos 5 secciones del espacio reservado 
para el objeto: La primera de estas (el offset 0) representa la posición en la que fue visitado ese tipo en un recorrido
DFS partiendo por el tipo Object y visitando todos los hijos de cada tipo (un recorrido por el árbol de jerarquía de
clases). La segunda sección es la encargada de representar el nombre de la clase, y lo que contendrá es la dirección
del segmento de datos donde está contenido. La tercera representa la cantidad de posiciones que ocupa ese objeto en
memoria, todas las clases a lo sumo ocupan 4 posiciones: 3 para estas 3 secciones que hemos visto y 1 para la próxima
sección. La cuarta sección es la dirección a donde está definido en memoria las funciones que son declaradas o heredadas
por la clase. Se detallará esto y luego se continuará con la quinta sección.

Existe un lugar en memoria donde están definidas las funciones que se heredan o declaran en cada clase, y estas
funciones están dispuestas en orden. La forma de ordenarlos es que la posición en la que se encuentra el nombre de esa
función va a ser la misma para todas las definiciones de funciones de otras clases que hay en memoria si estas clases 
se refieren a la misma función o a una redefinición de esta

La quinta sección contiene el valor de los atributos creados o heredados por la clase,
es la que cambia en tamaño. Cada una de las anteriores ocupaba 1 posición, sin embargo esta sección 
ocupará tantas posiciones como atributos se definan o hereden en la clase y la posición de los atributos en esta
sección importa. La forma de ordenarlos es similar al orden de los nombres de las funciones en las que se hablaba en el
párrafo anterior. Aquí se definirán primero los atributos heredados (en el orden que los tiene la clase padre) y luego
los atributos definidos en ella.

El offset se incrementa en 4 con cada posición, por lo que si queremos referirnos al valor del 
primer atributo de una clase A tendremos que referirnos al offset 16 (5ta posición (5-1)*4=16)

| Sección 1 | Sección 2 | Sección 3 |       Sección 4       | Sección 5 |
|:---------:|:---------:|:---------:|:---------------------:|:---------:|
| Id en DFS |  Nombre   |  Tamaño   | Dirección a funciones | Atributos |
 
Hasta ahora se ha visto la representación en memoria de los objetos, se verá ahora la estrategia para llamar funciones.
Para almacenar los argumentos de la función se utiliza la pila, son pusheados en orden contrario al que se piden
para que se puedan sacar en orden luego utilizando el stack pointer (registro $sp) como referencia. Las funciones
también definen variables temporales y para almacenarlas se utilizará también la pila, como la cantidad de locals se 
conoce en CIL entonces se conoce el espacio que ocupan y se conoce además el orden que tienen. Nuevamente se puede 
acceder a ellos usando el stack pointer que está contenido en el registro $sp. El valor de retorno de una función 
estará siempre contenido en el registro $a1.
