# Informe de Complementos de Compilacion
## Compilador de Cool
***


## Autores 
- Claudia Olavarrieta Martinez 
- Marcos Adrian Valdivie Rodriguez
- Adrian Hernandez Perez

## Uso del compilador

## Arquitectura del compilador 
 
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
Dentro del fichero mips_basics.asm 

### Organizacion

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

## Principales Problemas

