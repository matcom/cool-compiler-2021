# El modulo cool_compiler

Se componen de otros 5 modulos, cmp, lexer, parser, semantic, generator_code.
Menos cmp el cuale contiene implementaciones utiles aportadas por los profesores 
en el curso pasado, el resto mantienen la misma extructura para mantener un estado 
open-close coherente claro y flexible

 - `__init__.py` contiene las distintas implementaciones que pueden llegar a necesitar 
 un usuario de dicho modulo, y de esta manera abstraer al "mundo" del el contenido y 
 compisicion del mismo
 - `__dependency.py` en caso de ser necesario contienen los `import` de las implemetaciones
 externas al modulo que el mismo necesita para su funcionamiento (como pueden ser los utiles 
 del  modulo cmp)
 - `__main__.py` es una ruta de ejecucion para el modulo como un todo, cada caso particular 
  se puede usar para ejecutar codico externo en el proceso de implementacion. Y en el caso 
  particular del modulo cool_compiler supone la puerta de inicio de todo el proyecto

Para mayor legibilidad del del proyecto las `.py` que contienen caracteristicas destintivas 
del lenguaje de cool como pueden ser, tabla de expresiones regulares, gramatica, y AST semantico
se encuentran fuera de los distintos modulos en el nivel mas superficial del modulo cool_compiler. 
Para la consistencia de los distintos modulos como un todo, es necesario un consenso en la implementacion
de estas caracteristicas del lenguaje, pues:

- Primero, el tipo de los token debe coincidir con los no terminales de la gramtica, para lo que reunimos 
estos tipos en un `Enum`, `TokenType` en **table_regex.py**, unificando ambos conceptos para cualquier 
posible cambio. La implementacion y definicion de este `Enum` queda cargo del primero que lo necesite 
entre los desarolladores de parser y lexer, al momento de textear su codigo. Tras la definicion 
se debe actualizar el repo comun lo mas rapido posible para evitar errores
- Segundo, de igual manera sucede con los nodos del AST y la atributacion de la gramatica, y los modulos 
en este caso particular el desarrolador del parser debe "esperar" por el de semantic, aunque esta definicion
es el primer paso del desarrollo del modulo semantic  