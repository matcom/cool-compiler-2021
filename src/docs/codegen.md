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
\text{Expression} &\rarr& \text{id = AtomicOp}\\
&|& \text{goto id}\\
&|& \text{label id}\\
&|& \text{return Atom}\\
&|& \text{setattr id id Atom}\\
&|& \text{if Atom goto id}\\
&|& \text{ArgList id = call id}\\
&|& \text{ArgList id = vcall id id }\\
&|& \text{\{ExpressionList\}}\\
\text{ExpressionList} &\rarr& \text{Expression; ExpressionList } | \text{ Expression} \\
\text{ArgList} &\rarr& \text{arg id; ArgList } | \space\epsilon \\

\text{AtomicOp} &\rarr& \text{Atom + Atom}\\
&|& \text{Atom + Atom}\\
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
Remaining = {Let, Case }

