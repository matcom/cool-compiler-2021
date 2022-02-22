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
para luego ser usado por el parser. En esta fase se utilizo el paquete _ply_ el cual permite ...breve descripcion de ply... . Se definieron
las expresiones regulares y simbolos que correspondian a los tokens de la 
gramatica. Ademas se almacena por cada Token la linea y la columna correspondiente
en el codigo, lo que permite tener mayor informacion en los mensajes de error
y para nuestro uso en la depuracion.


#### Parser

#### Recoleccion de tipos

En esta fase se recorren todas las declaraciones de clases, se crean los tipos asociados
y se valida que no se este redefiniendo una clase. 


### Modulos

### Gramatica

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

