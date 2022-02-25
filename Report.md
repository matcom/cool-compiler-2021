# Cool Compiler Project

## Integrantes

- Thalía Blanco Figueras
- Nadia González Fernández
- José Alejandro Labourdette-Lartigue Soto

## Introducción

El proyecto presenta un compilador capaz de interpretar el lenguaje COOL 
"The Classroom Object-Oriented Language". La solución está desarrollada en python.

## Contenido


| Compiler Stage     | Python Module                                        |
|:-------------------|:-----------------------------------------------------|
| Lexical Analysis   | [lexer.py](/src/lexer.py)                            |
| Parser             | [parser.py](/src/parser.py)                          |
| Semantic Analysis  | [semantic_analyzer.py](/src/semantic_analizaer.py)  |
| Code Generation    | [mips_generator.py](/src/mips_genertor.py);          |


## Lexer y Parser
Para el desarrollo del lexer y el parser se utilizó la herramienta de parsing **PLY**.
Esta es una implementación en python de lex/yacc.

### Gramática
La Grámatica usada es libre de contexto y de recursión extrema izquierda. Debido a la forma
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
## Lexer
En la implementación del lexer se declaran los tokens, que definien todos los posibles tokens 
que el compilador recibirá. Esta lista también se utiliza en el parser. 
Estos tokens se definen con la expresión regular compatible con el módulo **re** de Python

**Ejemplo:**
```python
tokens = ['INTEGER',  # Non-empty strings of digits 0-9
          
          'PLUS', 'MINUS', 'MULT', 'DIV',
          ]

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

En la implementación del parser se utiliza `ast_hierarchy.py`.En este se definen los
nodos del árbol que se construirá en el parser. Las reglas de gramática mostradas 
anteriormente se definen en python:

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

## Análisis Semántico

Para el análisis semántico seguimos un patrón visitor. Se hacen 3 recorridos por el ast en esta fase:

- [Type Collector](/src/type_collector.py) 
- [Type Builder](/src/type_builder.py)
- [Type Checker](/src/type_checker.py)

En el typeCollector se hace un primer recorrido por el AST recolectando todos los tipos. También se añaden 
los tipos predefinidos por el lenguaje COOL.

En el TypeBuilder se analizan los parámetros, valores de retorno, y otras referencias a tipos. En esta fase 
se definen todos los atributos y las funciones y se hace el análisis sintáctico de la entrada.

En el typeChecker se hace el análisis semántico. En esta fase se recoleccionan y construyen los tipos. 
También se hace la inferencia de tipos.

A cada declaración de clase se le asocia un scope, y dicho scope tendrá referencia al scope de la clase padre 
en caso de que exista herencia.

## Generador de Código

### Cool -> CIL

### CIL -> MIPS
