# Informe de Complementos de Compilación
## Compilador de Cool
***


## Autores 
- Claudia Olavarrieta Martínez 
- Marcos Adrián Valdivié Rodríguez
- Adrián Hernández Pérez

## Uso del compilador

**Requerimientos**

Para ejecutar el proyecto es necesario instalar Python y las dependencias que 
se listan en requirements.txt

Para instalar las dependencias puede ubicarse en la carpeta del proyecto y ejecutar

```bash
pip install -r requirements.txt
```

**Ejecución**

Para ejecutar el proyecto debe situarse en la carpeta *src* y utilizar alguno de los
dos comandos que se muestran a continuación:
```bash
python Main.py -f path/to/file.cl 
python Main.py --file path/to/file.cl
```

Como salida se guarda en un fichero del mismo nombre del introducido como parámetro
con extensión *.mips* el código compilado y listo para ejecutarse. 

## Arquitectura del compilador 

El compilador está compuesto por distintos módulos que son los encargados de tomar 
el código escrito inicialmente en COOL y obtener el resultado final en código MIPS que 
permita su ejecución. 

## Organizacion

La estructura de archivos del proyecto es la siguiente:         
 
```
cool-compiler-2021
|___doc 
    img            
    src
     |__Main.py
        core
            |__cil
                   |__BaseCOOLToCilVisitor.py
                     CILAst.py
                     COOLToCILVisitor.py
            |__lexer
                   |__lexer.py
            |__mips
                   |__CilToMipsVisitor.py
                      mips_basic.asm
                      MipsAst.py
                      MIPSAstFormatter.py
            |__parser
                   |__Parser.py
            |__semantic
                   |__Type_Builder.py
                      Type_Checker.py
                      Type_Collector.py
            |__tools
                   |__automata.py
                      COOLAst.py
                      Errors.py
                      evaluation.py
                      First_and_Follow.py
                      Parser_LR1.py
                      parsing.py
                      pycompiler.py
                      Semantic.py
                      utils.py
                      visitor.py
        

```

Se omitieron algunos archivos pues no son relevantes en la implementacion del compilador.
 
### Fases (_Pipeline_)

El fichero _Main.py_ contiene el pipeline de ejecución del compilador
1. Lexer       
2. Parser     
3. Recolección de Tipos         
4. Construcción de Tipos        
5. Chequeo de Tipos
6. COOL a CIL
7. CIL a Mips
8. MIPS a representación como string
9. Escritura en el archivo final

#### Lexer 

El Lexer es el encargado de dado un string con el código del programa COOL separar el mismo en tokens
para luego ser usado por el parser. En esta fase se utilizó el paquete _ply_ el cual contiene 
herramientas de tokenización. Se definieron las expresiones regulares y símbolos que correspondian a los 
tokens de la gramática, definiendo reglas especiales para poder también reconocer los string y comentarios 
anidados. Además se almacena por cada Token la línea y la columna correspondiente
en el código, lo que permite tener mayor información en los mensajes de error
y para nuestro uso en la depuración.

#### Parser

El Parser define la estructura que tendrá el Árbol de Sintaxis Abstracta (AST) del lenguaje COOL, además
de la gramática que se usará para parsear este.        
El archivo donde se definen los símbolos y producciones de la gramática puede verse en 
[Gramatica COOL](https://github.com/NinjaProgrammers/cool-compiler-2021/blob/Proyecto-CMP/src/core/parser/Parser.py)

Se utilizó un parser LR1 que había sido implementado y probado en proyectos anteriores
de la asignatura. Fue necesaria la inclusión de nuevas reglas y la edición de algunas anteriores para la 
solución de problemas con la precedencia de los operadores y la ambiguedad de la gramática.
Durante esta fase se reconocen y reportan los errores léxicos del programa.

## Gramática

### Terminales
A continuación se muestran los terminales de la gramática, donde entre paréntesis se muestran
los símbolos que corresponden a COOL en los casos en que era requerido:

- *classx (class), inherits, function*
- *ifx (if), then, elsex (else), fi*
- *whilex (while), loop, pool*
- *let, inx (in)*
- *case, of, esac*
- *semi (;), colon (:), comma (,), dot(.), at (@), opar((), cpar ())*
- *ocur ({), ccur (}), larrow (<-), rarrow (=>)*
- *plus (+), minus (-), star (\*), div (/), isvoid, compl (~)*
- *notx (not), less (<), leq (<=), equal (=)*
- *new, idx (id), typex (type), integer, string, boolx (bool)*
 
 
### No Terminales

A continuación se muestran los no terminales de la gramática definida: 

- __program__ 
- __class_list, def_class__
- __feature_list, feature__
- __param_list, param__
- __expr_1, expr_2, member_call, expr_list, let_list, case_list__
- __comp_expr, arith, arith_2, term, factor, factor_2__
- __atom, func_call, arg_list__

### Producciones de la Gramática 
A continuación se muestran las producciones de la gramática. En *cursiva* se muestran los terminales
y en **negrita** los no terminales

__program__ ⟶ __class_list__

__class_list__  ⟶ __def_class  class_list__                 
__class_list__  ⟶ __def_class__

**def_class** ⟶ *class* *typex* { **feature_list** } ;       
**def_class** ⟶ *class* *typex* *inherits* *typex* { **feature_list** } ;         

**feature_list** ⟶ **feature feature_list**       
**feature_list** ⟶ 𝜺      

**feature** ⟶ *idx* : *typex* ;                      
**feature** ⟶ *idx* : *typex* <- **expr_1**;           
**feature** ⟶ *idx* (**param_list**) : *typex* { **expr_1** } ;            
**feature** ⟶ *idx* () : *typex* { **expr_1** };              
**feature** ⟶ **function** *idx* (**param_list**) : *typex* {**expr_1**};              
**feature** ⟶ **function** *idx* () : *typex* {**expr_1**};      

**param_list** ⟶ **param**              
**param_list** ⟶ **param** , **param_list**      

**param** ⟶ *idx* : *typex*

**expr_1** ⟶ *idx* <- **expr_1**         
**expr_1** ⟶ *not* **expr_1**          
**expr_1** ⟶ **expr_2** = **expr_1**        
**expr_1** ⟶ **expr_2**

**expr_2** ⟶ **arith** < **arith**    
**expr_2** ⟶ **arith** <= **arith**        
**expr_2** ⟶ **arith**

**arith** ⟶ **arith** + **factor**         
**arith** ⟶ **arith** - **factor**      
**arith** ⟶ **factor** 

**factor** ⟶ **factor** \* **term**        
**factor** ⟶ **factor** / **term**
**factor** ⟶ **term**

**term** ⟶ ~ **term**      
**term** ⟶  *isvoid* **term**     
**term** ⟶ **atom**

**atom** ⟶ (**expr_1**)            
**atom** ⟶ *string*        
**atom** ⟶ *bool*       
**atom** ⟶ *idx*     
**atom** ⟶ *ifx* **expr_1** *then* **expr_1** *else* **expr_1** *fi*         
**atom** ⟶ *whilex* **expr_1** *loop* **expr_1** *pool*           
**atom** ⟶ *new* *typex*    
      
**atom** ⟶ { **expr_list** }           
**expr_list** ⟶ **expr_1** ;          
**expr_list** ⟶ **expr_1** ; **expr_list**          

**atom** ⟶ *case* **expr_1** *of* **case_list** *esac*                      
**case_list** ⟶ *idx* : *typex* => **expr_1** ;                        
**case_list** ⟶ *idx* : *typex* => **expr_1** ; **case_list**          

**atom** ⟶ **func_call**               
**func_call** ⟶ **atom** @ *typex* . *idx* (**arg_list**)             
**func_call** ⟶ **atom** @ *typex* . *idx* ()                   
**func_call** ⟶ **atom** . *idx* (**arg_list**)        
**func_call** ⟶ **atom** . *idx* ()

**func_call** ⟶ *idx* (**arg_list**)       
**func_call** ⟶ *idx* () 

**arg_list** ⟶ **expr_list**
**arg_list** ⟶ **expr_list** , **arg_list**

#### Recolección de tipos

En esta fase se recorren todas las declaraciones de clases, se crean los tipos asociados
y se valida que no se estén redefiniendo estos. Primeramente se añaden los tipos builtin
(Object, IO, Bool, String, Int) y luego los tipos definidos por el usuario, revisando 
que no existan nombres de clases repetidos.

#### Construcción de Tipos

En esta fase se recorren nuevamente las declaraciones de clases añadiendo los métodos y 
atributos de cada clase. Se define la herencia para cada clase, en caso que no exista se hereda de la 
clase Object. Además se revisa que exista una clase Main con un método main que indica el inicio 
de la ejecución del programa COOL.

#### Chequeo de tipos

En esta fase se hace el chequeo semántico de cada tipo. Se evalúa para cada expresión su tipo de retorno
y se valida que estos cumplan las reglas semánticas definidas en el lenguaje. Además se chequea nuevamente
las clases definidas por el usuario en busca de la existencia de herencia cíclica.
Algunos de los errores que se chequean en esta fase son:
- Las operaciones aritméticas solo están definidas para el tipo Int.
- Que las variables y los métodos hayan sido definidos previamente a su uso.
- Que no exista redefinición de métodos o atributos en las clases.
- Que no exista herencia cíclica.
- Que las palabras claves self y SELF_TYPE sean usadas correctamente.
- Que las funciones de clases sean llamadas con la cantidad correcta de parámetros.
- Que el objeto usado en cada expresión sea compatible con el tipo declarado para la misma.

#### COOL a CIL

Durante esta fase se realiza la conversión del lenguaje COOL a un lenguaje intermedio(CIL). 
El fichero CilAst contiene la definición de las clases usadas para conformar el AST del lenguaje CIL. 
En el fichero BaseCOOLtoCILVisitor se definen los métodos básicos para registrar
una variable, parámetro, función y atributo, entre otros. Ademas se 
registran los tipos builtin, es decir, se escriben en código CIL las instrucciones
para registrar los tipos Object, IO, String, Int y Bool, así como las funciones y atributos de cada uno de estos..
El fichero COOLToCILVisitor es el encargado de transformar el AST de COOL en un AST de CIL, para facilitar
luego la traducción de este al lenguaje MIPS. Este fichero cuenta con un visitor que se encarga de transformar
cada nodo del AST de un lenguaje a otro, algunos de los aspectos a destacar son:
- En el visitor del ProgramNode se define la función entry, que es por donde se comenzará la ejecución del
programa MIPS.
- En el visitor del ClassDeclarationNode se definen las funciones init e init_attr corespondientes a cada
clase, estas funciones son las encargadas de reservar la memoria necesaria para cada uno de los tipos
definidos por el usuario.
- Especial énfasis en el visitor del CaseOfNode, este se encarga de generar todas las instrucciones
necesarias para validar correctamente la rama que debe ejecutarse, o mostrar un error en tiempo de ejecución
en caso de no haber ninguna válida. Para lograr esto primero se ordenan los tipo involucrados en las ramas del
case según su profundidad en el árbol de herencia del programa, de mayor a menor. Luego se visitan estos, 
revisando para cada uno todos sus descendientes en dicho árbol de herencia y comprobando, en tiempo de
ejecución, si estos coinciden con el tipo del objeto que se está analizando. El primer objeto para el que
se halle una correspondencia define la rama por la que debe continuar la ejecución del programa.
- En el visitor del DivNode se añaden las instrucciones necesarias para verificar que el divisor es distinto
de cero, y lanzar un error en tiempo de ejecución en caso contrario.
- El visitor del EqualNode se encarga de verificar primeramente los tipos de los objetos que están siendo 
comparados, Int-Int, String-String y Bool-Bool son comparados por valor, mientras que cualquier otro par
es comparado por referencia.
- El visitor del FunctionCallNode se encarga de verificar que el objeto al cual se le hace el dispatch sea
distinto de Void y mostrar un error en ejecución en caso contrario.

#### CIL a MIPS

Esta es la fase final donde se traduce de CIL al lenguaje MIPS que da la salida del programa.   
Dentro del fichero mips_basics.asm se encuentran algunas funciones predefinidas en mips: malloc, copy, 
read_string, equal_string, length, substring y concat.    
El fichero MIPSAst contiene la definición de las clases necesarias para representar el código MIPS.     
El fichero CILToMipsVisitor visita cada nodo del AST de CIL y lo traduce s su correspondientes 
instrucciones en codigo Mips. Gran dificultad trajo en esta fase el uso correcto de las tablas de dispatch
y los atributos de clase en combinación con la herencia, haciendo necesaria una especificación sobre la 
representación en memoria que tendría cada objeto. Sobre esto útimo podemos explicar que se decidió representar
los objetos como:
- Marca de clase (4 bytes): Un entero usado para identificar cada tipo del programa.
- Tamaño (4 bytes): Un entero usado para representar el tamaño, en doble palabras, de la representación del objeto
en memoria.
- Puntero a la tabla de dispatch (4 bytes): Un entero que representa la posición en memoria donde se encuentra 
la tabla de dispatch del objeto.
- Definición de atributos de la clase padre.
- Definición de atributos de la clase hijo. Primero son definidos los atributos de la clase padre de forma recursiva,
luego son definidos los atributos de la clase hijo, colocando estos de forma ordenada según los nombres que tenían
en el código COOL inicial.
Las tablas de dispatch de cada tipo se definen de forma similar, primero las direcciones de memoria correspondientes
a las funciones de las clases padres, o a las de la clase hijo en caso de que hayan sido redefinidas, y luego las
direcciones de memoria de las funciones de la clase hijo, ordenadas alfabéticamente según sus nombres iniciales. 
Finalmente las funciones init e init_attr de la clase correspondiente. Cada dirección de memoria corresponde a un
entero de 32 bits. El orden de las funciones en la tabla de dispatch inicia por las del padre para poder ejecutar
correctamente el llamado a una función redefinida en un objeto del tipo hijo cuando este es tratado como un
objeto del tipo padre (polimorfismo).

Finalmente, el fichero MIPSAstFormatter es el encargado de transformar el AST de MIPS a formato string para
luego escribir este en el archivo final.

## Licencia

[MIT](https://github.com/NinjaProgrammers/cool-compiler-2021/blob/Proyecto-CMP/LICENSE)


 
          





