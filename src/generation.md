# Generación

## Correr programa con spim

> $ spim -file "PROGRAMA.mips"

## Detalles

El direccionamiento de memoria es a base de bytes
Las words son 4 bytes

## Tipos

nombre: .word DIR_TIPO_PADRE, TAMANO_DE_INSTANCIA_BYTES [, LABEL_AL_METODO_i]

## Llamados

Los llamados dinámicos solo se usan en caso de que se utilice un SELF_TYPE, en otro caso se utilizan los estáticos. Cuando se va a crear un nodo de llamado dinámico se anota en él el tipo en donde fue definido el SELF_TYPE para luego poder resolver correctamente la dirección del método ya que bajo un mismo árbol de herencia el offset de los métodos no cambia.

## Llamados y el Stack

Para los llamados a funciones, primero se meten los argumentos en orden en la pila y se llama a la función. Luego dentro de la función se guardan las variables locales en la pila y luego se guardan los registros que se van a cambiar (ra y fp). Luego se reintegran los valores de los registros y se limpia la pila de las variables locales. Un TODO sería optimizar la generación tanto en el CIL como en MIPS, para no depender de las variables en la pila y trabajar más con los registros, esto aumentaría la velocidad y disminuye la cantidad de operaciones necesarias. Ej de pila:

PARAM1  
PARAM2  
PARAM3  
LOCALVAR4  
LOCALVAR3  
LOCALVAR2  
LOCALVAR1 <- Aquí estaría apuntando el FP de la función  
RA  
FP(Viejo)  

El stack crece para abajo:
0xfffffff  |         |
0xffffffe  |         |   |
0xffffffd  |         |  \ /
0xffffffc  |         |

O sea, se resta para crecer

## Instancias

Espacio de memoria de tamaño la cantidad de bytes que se lleva según la cantidad de atributos que posee el tipo.

### Organización en memoria

DIR_AL_TIPO [, VALOR_DE_ATRIBUTO]

## A tener en cuenta

1. Crear función de entrada main

```mips
main: # entrada

```

2. Recordar siempre cuando se termina llamar el syscall de exit

```mips
main: # entrada
    addi $v0, $zero, 10 # Argumento para la salida
    syscall # Salir
```

# Macros

No soportadas al parece por spim

```mips
.macro push($x)

addiu $sp, $sp, -4
sw $x, 0($sp)

.endmacro

.macro pop($x)

lw $x, 0($sp)
addiu $sp, $sp, 4

.endmacro


```