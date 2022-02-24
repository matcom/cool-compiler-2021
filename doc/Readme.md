# Informe de Complementos de Compilacion
## Compilador de Cool
***


## Autores 
- Claudia Olavarrieta Martinez 
- Marcos Adrian Valdivie Rodriguez
- Adrian Hernandez Perez

## Uso del compilador

**Requerimientos**

Para ejecutar el proyecto es necesario instalar Python y las dependencias que 
se listan en requirements.txt

Para instalar las dependencias puede ubicarse en la carpeta del proyecto y ejecutar

```bash
pip install -r requirements.txt
```

**Ejecucion**

Para ejecutar el proyecto debe situarse en la carpeta *src* y utilizar algun de los
 dos comandos que se muestran a continuacion
```bash
python Main.py -f path/to/file.cl 
python Main.py --file path/to/file.cl
```

Como salida se guarda en un fichero del mismo nombre del introducido como parametro
pero con extension *.mips* el codigo compilado y listo para ejecutarse. 

## Arquitectura del compilador 

El compilador esta compuesto por distintos modulos que estan encargados de tomar 
el codigo escrito inicialmente en COOL y obtener el resultado final en codigo MIPS que 
permita su ejecucion. 
 
### Fases (_Pipeline_)

El fichero _Main.py_ contiene los llamados en orden de los metodos que 
componen el pipeline de ejecucion del compilador
1. Lexer       
2. Parser     
3. Recoleccion de Tipos         
4. Construccion de Tipos        
5. Chequeo de Tipos
6. COOL a CIL
7. CIL a Mips

#### Lexer 

El Lexer es el encargado de dado un string con el código del programa COOL separar el mismo en tokens
para luego ser usado por el parser. En esta fase se utilizo el paquete _ply_ el cual contiene 
herramientas de parser en Python . Se definieron
las expresiones regulares y simbolos que correspondian a los tokens de la 
gramatica. Ademas se almacena por cada Token la linea y la columna correspondiente
en el codigo, lo que permite tener mayor informacion en los mensajes de error
y para nuestro uso en la depuracion.


#### Parser

El Parser define la estructura que tendrá el Árbol de Sintaxis Abstracta (AST) de la aplicación, además
de la gramática que se usará para parsear el código COOL dado.        
El archivo donde se definen los simbolos y producciones de la gramatica puede verse en 
[Gramatica COOL](https://github.com/NinjaProgrammers/cool-compiler-2021/blob/Proyecto-CMP/src/core/parser/Parser.py)

#### Recoleccion de tipos

En esta fase se recorren todas las declaraciones de clases, se crean los tipos asociados
y se valida que no se este redefiniendo una clase. Primeramente se annaden los tipos builtin
(Object, IO, Bool, String, Int) y luego se anaden los tipos definidos por el usuario, revisando 
que no existan nombres de clases repetidos.

#### Construccion de Tipos

En esta fase se recorren nuevamente las declaraciones de clases annadiendo los metodos y 
atributos de cada clase. Se encarga de definir la herencia, en caso que no exista se hereda de la 
clase Object. Ademas se revisa que exista una clase Main con un metodo main que indica el inicio 
de la ejecucion del programa COOL.

#### Chequeo de tipos

En esta fase se revisa la compatibilidad de tipos (Ej: que no se sume int y string), que variables
o metodos hayan sido definidos previamente, correctitud de la herencia (que no exista herencia ciclica)
 
#### COOL a CIL

Durante esta fase se realiza la conversion del lenguaje COOL al lenguaje intermedio
CIL.      
En el fichero BaseCOOLtoCILVisitor se definen los metodos basicos para registrar
una variable, parametro, funcion, atributo, entre otros. Ademas es aqui donde se 
registran los tipos builtin, es decir se escriben en codigo CIL las instrucciones
para registrar los tipos Object, IO, String, Int y Bool.
El fichero COOLToCILVisitor .... ????????

#### CIL a MIPS

Esta es la fase final donde se traduce del lenguaje intermedio al lenguaje MIPS que 
es el que va a ser ejecutado.   
Dentro del fichero mips_basics.asm se encuentran funciones predefinidas en mips:
Malloc, Copy, Read String, Equal String, Length, Substring y Concat.         
En CILToMipsVisitor se visita cada nodo del arbol de CIL y se traduce la instruccion
a las correspondientes instrucciones en codigo Mips.


  
## Principales Problemas



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


## Gramatica

### Terminales
A continuacion se muestran los terminales de la gramatica, donde entre parentesis se muestran
los simbolos que corresponden a COOL en los casos en que era requerido:

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

A continuacion se muestran los no terminales de la gramatica definida: 

- __program__ 
- __class_list, def_class__
- __feature_list, feature__
- __param_list, param__
- __expr_1, expr_2, member_call, expr_list, let_list, case_list__
- __comp_expr, arith, arith_2, term, factor, factor_2__
- __atom, func_call, arg_list__

### Producciones de la Gramatica 
A continuacion se muestran las producciones de la gramatica. En *cursiva* se muestran los terminales
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

## Licencia

[MIT](https://github.com/NinjaProgrammers/cool-compiler-2021/blob/Proyecto-CMP/LICENSE)


 
          





