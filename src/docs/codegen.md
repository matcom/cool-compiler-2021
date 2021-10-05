# Generacion de Codigo

Despues de realizado el chequeo semantico se procede a realizar la generacion de codigo con el ast obtenido como resultado.

Se utiliza un nuevo ast para esta parte del compilador _codegen_ast.py_. 

Cada nodo de este nuevo AST se representa a si mismo en cil.

### Program Node \<program>

```
.TYPE
<type 1>
<type 2>
...
<type n>

.DATA
<str 1>
<str 2>
...
<str m>

.CODE
<attr_info 1>
<attr_info 2>
...
<attr_info q>
<func_info 1>
<func_info 2>
...
<func_info p>
```

### Class Declaration Node \<type>

```
<attr 1>
<attr 2>
...
<attr n>
<func 1>
<func 2>
...
<func m>
```

### Function Declaration Node \<func>

```
todo
```

### Function Declaration Node info() <func_info>

```
todo
```

### Attribute Declaration Node \<attr>

```
todo
```

### Attribute Declaration Node info() \<attr_info>

```
todo
```

