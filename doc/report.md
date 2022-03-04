# Reporte sobre el Compilador de Cool

## Uso del compilador

El `Compilador de Cool` implementado es un programa en lenguaje **Python**; programa que tiene
como función principal dada la dirección de un archivo tipo `"file.cl"`, que contenga un programa
de **Cool**, analizar dicho fichero reportar errores si tiene, en caso contrario generar un nuevo
fichero en la misma direccilón en esta ocación terminado en `".mips"`. El programa se puede ejecutar
con el commando:

        python -m cool_compiler <file_dir>

En implementación del compilador se utilizo la librería **sly**, en especifico la version 0.4, la misma
debe ser instalada previo a la ejecución del programa. Para instalar dicha librería se debe correr el comando:

        pip install sly==0.4

## Arquitectura del compilador

El compilador es un único gran módulo `cool_compiler`, que contiene otros 7 módulos más:

### 1 - Módulo Cmp

Módulo aportado por los profesores de la asigantura, cuyas impelmentaciones ha servido de
apoyo para las distintas clases practicas y proyectos a lo largo del curso. De este módulo
se utilizan principalmente las clase `Type` y `Scope`, asi como los decoredores necesarios para
implementar el patrón **visitor**. A dichas implementaciones a lo largo del desarrollo se le
realizarón pequeñas modificaciones para ajustarlas, más aun, a las necesidades del desarrollo:

- __@visitor.result__: Nuevo decorador que se agregó a los decoradores del patrón visitor.
  Este decorador recibe la clase que sera el resultado de la funcion a la cual decora, una vez
  dicha funcion concluye sus valores de retorno son utilizados para instanciar la clase en
  cuestion. Además pasa del nodo de entrada hacia el nuevo nodo resultante la informacion
  sobre a que linea y columna pertenecen dichos nodos en el codigo original

### 2 - Módulo Lexer

Módulo que comienza con el analisis de código de cool que se desea compilar, su función principal
es convertir la cadena de caracteres en una cadena de token. Los token son la primera abstracción
que se le aplica al código, estos son subcadenas que son lexicograficamente significativas y según
este significado se les asigan un tipo (literal, keyword, type, identificador, number, string, etc).
El desarrollo de este módulo se apoyo en la libreria **sly**; expecificamente la clase **Lexer**, la cual
brinda la facilidad de definir un automata que reconozca las subcadenas significativas para un
lenguaje dad. Heredando de la clase **Lexer** y definiendo las propiedades _literals_ y _tokens_ se
puede expersar la lista de expersiones regulares que el automata debe reconocer, en este caso en
particular se definieron de la siguiente manera:

```python
    ...
    tokens = {
        CLASS, INHERITS,
        IF, THEN, ELSE, FI,
        LET, IN,
        WHILE, LOOP, POOL,
        CASE, OF, ESAC,
        ISVOID, NEW, NOT,
        TRUE, FALSE,
        ID, NUMBER, TYPE,
        ARROW, LOGICAR, LESS_OR,
        STRING
    }

    literals = {
        '{','}', '@', '.', ',', ';',
        '=', '<', '~', '+', '-',
        '*', '/', '(', ')', ':',
    }
    ...
```

La propiedad _tokens_ de la clase que hereda de **Lexer**, por defecto interpreta que los typos de
token definidos en la lista se le deben asignar a toda ocurrencia literal de dicho tipo, obviando si los
caracteres se encuentran en mayuscula o no. En caso en que el comportamietot por defecto no se ajuste
a las necesidades del lenguaje, **sly** permite que se redefina la expresion regular asignada a los typos
de token definidos (por ejemplo en el caso de cool los token ID y STRING). La sintaxis para refefinir
la expresion regular, es definiendole a la clase que hereda de **Lexer** una propiedad igual al tipo de
token que quiere redefinir:

```python
    ...
    ID      = r'[a-zA-Z][a-zA-Z0-9_]*'
    STRING  = r'\"'
    ...
```

Otra de las grandes ayudas que aporta **sly** que la facilidad de definir un método que se llamará al
momento una ocurrencia de un tipo de token determinado. De esta manera se pueden definir nuevos
comportamiento y personalizar el analisis del automata. Para explotar esta caracteristica de la libreria
basta con definir un metodo dentro de la clase con nombre igual a al tipo de token al que desea reaccionar

```python
    ...
    def STRING(self, token):
        lexer = CoolString(self)
    ...
```

Esta facilidad resultó muy útil para manejar el reconocimiento de los string y los comentarios de **Cool**.
Para estos dos casos se definieron otras dos clase que hereda de **Lexer** para darle un analisis diferenciado.
Estos fragmentos de código tiene un comportamientos similares al lenguaje `(ab)*` el cual no es regular, por lo
cual no basta con un automata finito determinista para reconocer todo el lenguaje. Para completar el reconocimiento
de estos fragmentos, apoyados en **sly**, se impelmentaro automatas con manipulación de memoria y asi poder contar
la cantidad de ocurrencias de los distintos delimitadores

### 3 - Módulo Parser

El módulo Parser se encarga de checkear la consistencia sintáxtica del código en cuestión. Dicho módulo tambien fue
implementado con la ayuda de **sly**, expecificamente con su clase **Parser**. Esta clase facilita la definición de
gramáticas atributadas de manera extremadamente comoda. Heredando de **Parser** se pueden definir métodos como
atributo de cada produccion de la gramatica y mediante el decorador **@\_** se expecifica la produccion a la que se le
debe asignar dicho atributo. Ejemplo:

```python
    # cclass: no terminal y epsilon terminal
    # en prod.cclass se encuentra el resultado del no teminal cclass
    # en prod.epsilon se encuentra el teminal epsilon
    @_("cclass epsilon")
    def class_list(self, prod):
        return [prod.cclass]
```

Además **Parser** ofrece las herramientas para desambiguar en casos en que exista colisiones entre las producciones,
como por ejemplo las producciones que tiene como cabezera el no terminal `expressionn`. Para que el parser sepa decidir
cual de las producciones se debe seleccionar en cada escenario se necesita definir una prioridad entre las producciones.
Para definir las presedencias de los distintos operadores, la clase **Parser** tiene la propiedad **precedence**, tupla de
tuplas ordenadas de menor a mayor precedencia. Dicha propiedad inicialmente se encuentra vacia, y de ser necesario se pueden
redefinir, en el caso particular del compilador de cool se redefinio de la manera siguiente:

```python
    ...
    precedence = (
        ('right', 'ARROW'),
        ('left','NOT'),
        ('nonassoc', '=','<','LESS_OR'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', "ISVOID"),
        ('left', '~'),
        ('left', '@'),
        ('right', 'IN'),
        ('left', '.'),
    )
    ...
```

Aprovechando la caracteristica de que la gramatica se encuentra recogida en una clase, se desarrollaron algunas herramientas
para realizar la inversion de la dependencia entre la gramatica y el ast, mediante el patrón **Factory**. Desde el módulo
parser se definió un enum con los nombres de los nodos que la clase parser le pasará a la fatoria de nodos, además de un
decorador que enlace un método con el nombre del nodo que el mismo creará




#generacion de codigo Mips
Para el inicio de la creación de código Mips partimos de la base de una librería escrita en este lenguaje la cual contendría gran parte de las herramientas con las que no apoyaríamos y así nos evitábamos la doble escritura del código . La librería es una herramienta simple , en ella se encuentra a modo de macro la implementación de todas las funcione de IO , como IO_out_string,IO_in_Int ,entre otras, las cuales tratábamos como funciones nativas o especiales, dado que en la conversión de CIL no teníamos contemplado el desglose de la implementación de estos métodos , solo detectamos que hay un llamado a estos e inmediatamente tenemos preconcebido el código asociado. Además  de las de tipo , entrada y salida de información , tenemos otras macros, las correspondientes al tipo string ,como substring , concat, lenght , las cuales se muestran en la documentación como funciones integradas a este tipo. Otras macro  en esta librería van asociadas al tipo object y a sus métodos como Copy , Abort y Type Name.
Se utilizó  una creación de tipo Int , Bool , String , la cuales contienen en su primera palabra la caracterización del tipo y en la segunda la propiedad value del tipo , por lo que en cada utilización de alguna operación que involucre alguno de estos tipos, son tratados de esta manera y siempre que se tenga una salida de algún dato de este tipo , se reserva memoria y se crea una nueva instancia que sera el valor de retorno.
Las operaciones entre los tipos enteros , no las podiamos realizar de manera natural debido a la representación que describimos anteriormente , por lo que también tenemos predefinidas los métodos básicos de operaciones aritméticas tomando como entrada los registros de propósito general $a0 y $a1 , dentro de esta se enmascara un poco el paso intermedio que se realiza antes de llegar a la manera natural de resolver las operaciones y creando un tipo nuevo de entero como resultado. De manera similar ocurre con las comparaciones que devuelven un valor de verdad. La relevancia de esta manera de tener los datos nos ayudó bastante para tener un chuequeo del tipo utilizado y simplificar algunas especificidades del lenguaje COOL.

A la hora de recorrer el código intermedio centramos nuestra conversión en crear una definición de cada clase , con sus funciones y atributos, ademas del nombre y luego las instancias de estas, las cuales se salvaban y mantenían validas en el programa a través de la pila. Posteriormente se desarrolla el código especifico de cada función utilizada y se utilizan los saltos para entrelazar mas de una.A continuacion mostramos un ejemplo de la representacion en codigo Mips de la clase Main:

```python
	Main_Name: .asciiz "Main"
	Main: .word Main_Name, 4, Main_parents, Object_abort, Object_copy, Object_type_name, IO_in_int, IO_in_string, IO_out_int, 		IO_out_string, Parse_read_input, Parse_parse_line, Parse_c2i, Parse_a2i, Parse_a2i_aux, Main_main, 

    .....

```

Otro punto importante en la generación de nuestro código Mips  fue la utilización de la pila y el mapeo que utilizamos a alto nivel para mantener un orden en esta. La creación de la clase “Stack” es la estructura encargada de que los parámetros recibidos y los puntos de retornos de los saltos fueran los correctos entre llamado, la cueal cuenta con lo siguiente:

```python
    ...
    class Stack:
    def __init__(self, node) -> None:
        self.name = node.name
        self.init_size = len(node.param) + len(node.local) + 1
        self.list = []
        self.local_push = 0 
    .....

```


 La estructura contiene unos métodos los cuales se encargan de su llenado y vaciado siempre teniendo en cuenta que cada dato era insertado de 4 en 4 con respecto al registro $sp. Cada argumento de las funciones son pasados a la pila antes de su llamado siendo luego los métodos los encargados de utilizarlos y dejar la pila , luego de su culminación , sin estos elementos. EL cambio del valor del $ra fue un tema importante con el que nos topamos por lo que también seguimos la linea de ponerlo dentro de la pila y luego asignándoselo al nuevo $ra para que la función pudiera retornar al punto especifico donde fue llamado y no creara conflictos.

