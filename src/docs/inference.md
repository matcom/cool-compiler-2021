# Inferencia

Se infieren los tipos  lo mas posbile aplicando las reglas de la semantica de cool. Cuando el inferenciador debe elegir entre varios tipos a asignar a una variable, escoge el mas general. El inferenciador da errores si entre los tipos que tiene a esocoger existe alguno que no tiene un ancestro comun mas general con los demas.

## Funcionamiento

El inferenciador se ejecuta varias veces, en cada una  realizando un chequeo distinto.

### Soft Inferencer 

Infiere el tipo de la expresion a base del tipo de la variable a la que esta asignada. Ya sea como asignacion o el valor de retorno esperado de una funcion.

Aplica las reglas de cool para realizar la infererencia.  Este permite que haya ambiguedad y que un tipo por determinar puede tener varios ancestros sin nada en comun.

En el lenguage cool esto se evidencia cuando se hace un llamado a una funcion del estilo

```
a.func();
```

donde el tipo de _a_  no es definido. El inferenciador buscara todas las clases con un metodo de nombre func y cantidad de parametro determinad y los tendra como posibles tipos para _a_. En estos casos _a_ puede ser de varios tipos no relacionados por ejemplo cuando:

```
class A {
	method func():Int{
		3 + 3
	}
};
class B {
	method func():String{
		"3 + 3"
	}
};
```

$a \in \{A, B\}$ donde A hereda de B y viceversa $a \notin \text{Object}$. pues Object no tiene un metodo func que recibe 0 argumentos.

Debido a que las variables pueden tener varios tipos no relacionados tampoco se revisa las comparaciones de igual.

### Hard Inferenecer

Infiere el tipo de la expresion a base del tipo de la variable a la que esta asignada. Ya sea como asignacion o el valor de retorno esperado de una funcion.

En esta parte el inferenicador realiza las misma acciones que en el Soft Inferencer, excepto que ya una variable $a$ no puede tener tipos de datos no relacionados.  Se revisa que las comparaciones de igualdad que ambos miembros sean del mismo tipo.

### Back Inferencer

Este se encarga de inferir el tipo de una variable a base del valor de la expresion.
