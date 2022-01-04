# Generacion de Codigo Intermedio

Despues de realizado el chequeo semantico se procede a realizar la generacion de codigo con el ast obtenido como resultado.

Se utiliza un nuevo ast para esta parte del compilador _codegen_ast.py_. 

Cada nodo de este nuevo AST se representa a si mismo en ccil (cool cows intermediate language).
$$
\begin{array}{rcl}
\text{Program} &\rarr& \text{.type TypeList .code CodeList}\\
\text{TypeList} &\rarr& \text{Type } | \text{ Type TypeList}\\
\text{Type} &\rarr& \text{FeatureList}\\
\text{FeatureList} &\rarr& \text{Attribute } | \text{ Function } | \text{ FeatureList } | \space\epsilon\\
&|& \text{ Attribute; FeatureList } | \text{ Function; FeatureList}\\
\\
\text{CodeList} &\rarr& \text{AttrCode }|\text{ FuncCode }|\text{ CodeList }| \space\epsilon\\
&|& \text{ AttrCode; CodeList } | \text{ FuncCode; CodeList}\\
\text{AttrCode} &\rarr& \text{id }\{ \text{LocalList Expression} \}\\
\text{FuncCode} &\rarr& \text{id }\{\\
&&\text{ParamList}\\
&&\text{LocalList}\\
&&\text{Expression}\\
&&\text{\}}\\
\\
\text{Expression} &\rarr& \text{id = ReturnOp}\\
&|& \text{goto id}\\
&|& \text{label id}\\
&|& \text{return Atom}\\
&|& \text{setattr id id Atom}\\
&|& \text{if Atom goto id}\\
&|& \text{ifFalse Atom goto id}\\
&|& \text{ArgList id = call id integer}\\
&|& \text{ArgList id = vcall id id integer }\\
&|& \text{ExpressionList}\\
\text{ExpressionList} &\rarr& \text{Expression; ExpressionList } | \text{ Expression} \\
\text{ArgList} &\rarr& \text{arg id; ArgList } | \space\epsilon \\

\text{ReturnOp} &\rarr& \text{Atom + Atom}\\
&|& \text{Atom - Atom}\\
&|& \text{Atom * Atom}\\
&|& \text{Atom / Atom}\\
&|& \text{not Atom}\\
&|& \text{neg Atom}\\
&|& \text{Atom < Atom}\\
&|& \text{Atom <= Atom}\\
&|& \text{Atom = Atom}\\
&|& \text{allocate id}\\
&|& \text{getattr id id}\\
&|& \text{Atom}\\
\text{Atom} &\rarr& \text{Constant } | \text{ id}\\
\text{Constant} &\rarr& \text{ integer } | \text{ string } | \text{ boolean }
\end{array}
$$

## Transformaciones

#### Program Declaration

**Cool Input**

```haskell
class A1 { ... }
class A2 { ... }
...
class AN { ... }
```

**CCIL Output**

```assembly
<class_A1_attr_and_func_declaration>
...
<class_AN_attr_and_func_declaration>

# Pending, should string literals be added here?
<all_constant_data_from_program>

<all_code_from_class_A1>
...
<all_code_from_class_AN
```

#### Class Declaration

En que momento se ejecuta la inicializacion de los atributos?

**Cool Input**

```haskell
class C {
	-- Initialized attributes
    a1: <attr_type> <- <expression>;
    a2: <attr_type> <- <expression>;
    ...
    am: <attr_type> <- <expression>;
    -- Uninitialized attributes
    aq: <attr_type>;
    ...
    ak: <attr_type>;
    
    -- Functions
	f1(<param_list>) { <expression> }
    f2(<param_list>) { <expression> }
    ...
    fn(<param_list>) { <expression> }
    
}
```

**CCIL Output**

```assembly
type C {
	# Initialized and uninitialized attributes together
	attribute a1;
	...
	attribute am;
	attribute aq;
	...
	attribute ak;
	
	method f1 : <func_code_name>;
	...
	method fn : <func_code_name>;
}
```

#### Class Inheritance

Se annade sobre la que ya tiene A, como se maneja la memoria, se annaden los atributos de B, despues de las funciones de A, o despues de los atributos de A

**Cool Input**

```haskell
class A {
	
}

class B inherits A {

}
```

**CCIL Output**

```
```



#### While Loop

**Cool Input**

```
while (<cond_expr>) loop <expr> pool
```

**CCIL Output**

```assembly
label while_init
x = <resultado_numerico_de_cond_expr>
ifFalse x goto while_end

<do_body_expr>

goto while_init
label while_end
```

#### If Then Else

**Cool Input**

```
if <if_expr> then <then_expr> else <else_expr> fi
```

**CCIL Output**

```assembly
x = <resultado_numerico_de_if_expr>
ifFalse x goto else_expr
label then_expr

<do then_expr>

goto endif
label else_expr

<do_else_expr>

label endif
```

#### Let In

**Cool Input**

```
let <id1>:<type1>, ... <idn>:<typen> in <expr>
```

**CCIL Output**

```assembly
<init id1>
<init id2>
...
<init idn>

# Si existe alguna variable let inicializada con una expresion, ejecutar dicha expresion
<do_idq_expr_and_save_to_idq>
<do_idk_expr_and_save_to_idk>
...
<do_idm_expr_and_save_to_idm>

<do_expr>
```

#### Case Of

**Cool Input**

```
case <case_expr> of
	<id1>:<type1> => <expr1>
	<id2>:<type2> => <expr2>
	...
	<idn>:<typen> => <exprn>
esac
```

**CCIL Output**

```assembly
<init id1>
<init id2>
...
<init idn>

<do_case_expr>
x = <case_expr_result>
t = typeof x
label init_case
t1 = typeof <id1>
b1 = t1 == t
if b1 goto branch1

t2 = typeof <id2>
b2 = t2 == t
if b2 goto branch2

...

tn = typeof <idn>
bn = tn == t
if bn goto branchn

label branch1
<do_expr1>
goto end_case

label branch2
<do_expr2>
goto end_case

...

label branchn
<do_exprn>
goto end_case

label end_case
```

El typeof tambien se conforma con un ancestro.  Que evaluaria la operacion de igualdad para escoger la rama adecuada? Lanzar un runtime error si no se escoge ninguna rama(eso puede pasar despues del cheque semantico?)

#### Function Static Call

**Cool Input**

```
<func_id>(<arg1>, <arg2>, ..., <argn>);
```

**CCIL Output**

```assembly
<init arg1>
<init arg2>
...
<init argn>
r = call <func_id> n
```

#### Function Dynamic Call

**Cool Input**

```
<type1>@<type2><func_id>(<arg1>, <arg2>, ..., <argn>);
```

**CCIL Output**

```assembly
<init arg1>
<init arg2>
...
<init argn>
t = allocate <type2>
r = vcall t <func_id>  n
```

#### Method Declaration

**Cool Input**

```
<function_id>(<arg1>:<type1>, ..., <argn>:<typen>) : <return_type>
{
	<function_expression>
}
```

**CCIL Output**

```assembly
function <function_id> {
	param <arg1>
	param <arg2>
	...
	param <argn>
	local <id1>
	local <id2>
	...
	local <idn>
	<do_expresion>
	r = <expression_result>
	return r
}
```

#### Expression Block

**Cool Input**

```
{
	<expr1>;
	<expr2>;
	...
	<exprn>;
}
```

**CCIL Output**

```
<init expr1 locals>
<init expr2 locals>
...
<init exprn locals>

<do_expr1>
<do_expr2>
...
<do_exprn>
```

