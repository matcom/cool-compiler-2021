# Inferencia

La idea principal para realizar la inferencia es considerar todo declaración como AUTO_TYPE no como un tipo especifico sino como un conjunto de tipos, donde inicialmente ese conjunto esta compuesto por todos los tipos definidos en un programa Cool. Los tipos declarados específicamente como Int o String se consideran conjuntos con un solo elemento.

La inferencia se realiza varias veces por visitores distintos que explicaremos mas adelante. En nuestra implementación debido a que le inferencia se apoya fuertemente sobre el reglas semánticas, el chequeo semántico se realiza a la par durante la inferencia, distribuido a lo largo de los visitores.

En el COOL original la mayoría de los nodos del árbol tienen un tipo estático declarado al igual que una expresión, donde el tipo de dicha expresión debe conformarse con el tipo estatico. Este es el caso para la declaracion de variables, la asignacion, cuando se pasan como argumentos, o una expresion con el retorno declarado.

Cuando el valor declarado es un tipo bien nombrado (diferente de AUTO_TYPE) y el valor inferido es un conjunto de tipos se truncan los que no conforman con el tipo estatico

Cuando el valor declarado es un tipo auto type, entonces tiene que ser algo a lo que se pueda conforma el expresion type

Cuando ambos son autotypes, ambos tienen que conformarse entre ellos, pero la cosa se pone sucia

Por estas razones el inferenciador se debido en dos partes, la primera parte trata de conformar los autotypes al tipo declarado (ya este sea otro autotyepe).

Esta primera parte se divide en dos partes tambien, una que llamamos inferencia suave, donde el conjunto de tipos puede tener elementos disjuntos y no se aplican casi reglas del chequeo semantico

La segunda parte de la primera parte llammos inferencia dura, donde no se es permisivo con violaciones de la regla semantica. Una vez termiando este recorrido, el conjunto de valores de expresiones debe estar lo mas reducido posible.

En la segunda parte falta reducir los conjutnos de elementos que se han declarado estaticamente como autotypes. (Ojo estos elementos pueden haberse reducido antes de llegar aqui si participan en una operacion aritmetica o dispatch).  (Este se ejcuta n veces, xq era?)

Luego de de terminar la inferencia se recorre un utlimo vistor. Este setea los tipos de acuerdo a su ancestro comun mas cercano. 

Se infieren los tipos  lo mas posbile aplicando las reglas de la semantica de cool. Cuando el inferenciador debe elegir entre varios tipos a asignar a una variable, escoge el mas general. El inferenciador da errores si entre los tipos que tiene a esocoger escoge siempre el mas general, el tipo raiz de todos. En caso de que sea para valor de retorno de un parametro, esocoge el "menor" ancestro comun.

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
class Main {
	a : AUTO_TYPE;
	method main():AUTO_TYPE {
		a.func()
	}
}

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

### Types Inferencer

Pasa una ultima vez por todas las expresiones 
