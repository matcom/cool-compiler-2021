# Semántica e Inferencia

Nuestro proyecto hace uso de `AUTO_TYPE` con la que incorpora inferencia de tipos al lenguage Cool. La inferencia se realiza varias en distintos vistores. En nuestra implementación debido a que le inferencia se apoya fuertemente sobre el reglas semánticas, el chequeo semántico se realiza a la par que la inferencia, y dividido de igual manera por los visitores.

La idea principal para realizar la inferencia es considerar todo declaración como `AUTO_TYPE` no como un tipo específico sino como un conjunto de tipos, donde inicialmente ese conjunto esta compuesto por todos los tipos definidos en un programa Cool. Los tipos declarados específicamente como `Int` o `String` se consideran conjuntos con un solo elemento.

En  Cool muchas veces las expresiones se ven obligadas a conformarse a un tipo definido por el usuario. Deben corresponder con el tipo definido de una variable, argumento o retorno de una función. También debe obedecer las reglas semánticas, cuando están presente frente a una operación aritmética, o en una posición donde se espera que el resultado sea `Bool`. Para reducir los conjuntos de tipos en presencia de `AUTO_TYPE` realizamos lo siguiente:

1. Cuando el tipo declarado de una variable esta bien definido (diferente de `AUTO_TYPE`) , se eliminan  del conjunto de tipos inferidos de la expresión los elementos que no conforman a dicho tipo bien definido.

2. Cuando el tipo declarado de una variable es `AUTO_TYPE`, esta se puede reducir analizando que valores debe tener para conformarse con los tipos de la expresión inferida.

3. Cuando ambos tipos, tanto el definido como el inferido son `AUTO_TYPES` se busca que valores puede tener el segundo para conformarse al primero, y que valores el primero para que el segundo se conforme.

Para tratar cada caso el inferenciador se divide en tres partes:

1. **soft inferencer** que aplica la primera regla y tercera regla. Se le llama **soft** porque perdona y no realiza ningún tipo de chequeo semántico y permite cosas como que un conjunto  tengo dentro de si dos tipos sin un ancestro común.
2. **hard inferencer ** aplica la primera y la tercera regla, y fuerza el chequeo semántico sobre todas las expresiones. No permite tipos sin ancestros comunes dentro de un mismo conjunto.
3. **back inferencer** aplica la segunda y tercera regla. Dada las expresiones trata de reducir los conjuntos de los tipos definidos como `AUTO_TYPE` (e.g. parámetros de una función, retorno de una función, o declaración de  variables)
4. **types inferencer** reduce todos los conjuntos de tipos de cada nodo al mayor ancestro en todos los casos, excepto cuando se trata del valor de retorno de una función, en el que reduce al ancestro común más cercano de los tipos del conjunto.

Cada inferenciador se ejecuta secuencialmente, una sola vez, exceptuando por el **back inferencer** que puede ejecutarse tantas veces como sea necesario.

## Soft Inferencer

El **soft inferencer** es permisivo pues como es el primero en leer el programa, puede que un conjunto de tipos inválidos en la línea 5 se vuelva válido más adelante en el código.

En este ejemplo no funcional (Lanza `RuntimeError` debido a que `a` es `Void`) donde el tipo de `a`  puede ser cualquiera, al leer `a.f()`, se reducen los tipos de a de  {`Object`, `String`, `IO`, `Int`, `Bool`, `Main`, `A`, `B`} a tan solo {`A`, `B`}. No obstante `A` y `B` no tienen un ancestro común dentro del conjunto, luego `a` posee un tipo invalido.

Luego cuando se lee `a.g()` el conjunto de tipos se reduce a  solo {`A`}.

```c#
class Main {
	a : AUTO_TYPE;
	method main():AUTO_TYPE {
		{
			a.f();  // Boom si no es el soft inferencer
			a.g();  // Solucionado
		}
	}
}
class A {
	method f():Int{
		3 + 3
	}
	metod g():String{
		"yisus"
	}
	
};
class B {
	method f():String{
		"3 + 3"
	}
};
```

## SELF_TYPE

La combinación de `SELF_TYPE` con `AUTO_TYPE` trajo sus problemas, sobre todo porque funciona como un comodín que puede tener un tipo dependiendo de las circunstancia. Logramos una mejor integración entre estos fue posible intercambiando el `SELF_TYPE` por la clase donde se encuentra analizando en ese momento.
