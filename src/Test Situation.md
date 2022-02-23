# Situacion de los test

## Lexer

- All OK

## Parsing

- All OK

## Semantic

- All OK

## Generation

### Fallando

- arith.cl
  - Funciona si se le pasa el input con \< o a mano escribiendo en la consola.
  - En el test el output devuelve un string muy largo sin razon evidente
- life.cl
  - Funciona si se le pasa el input con \< o a mano escribiendo en la consola.
  - El output es el mismo que el esperado.
- palindrome.cl
  - Funciona si se le pasa el input con \< o a mano escribiendo en la consola.
  - El output es el mismo que el esperado.
- prime.cl
  - Funciona si se le pasa el input con \< o a mano escribiendo en la consola.
  - Al output al parecer le falta un cambio de linea al final. En lo demás es el mismo que el esperado
- print-cool.cl
  - No funciona
    - Exception occurred at PC=0x004002c0
    - Bad address in data/stack read: 0x00000000
- graph.cl
  - No funciona
    - Un ciclo de Bad address in text read: 0x...
- hairyscary.cil
  - No funciona
    - Can't expand stack segment by 8 bytes to 524288 bytes
    - Use -lstack # with # > 524288
