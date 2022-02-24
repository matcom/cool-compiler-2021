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
- graph.cl
  - Funciona si se le pasa el input con \< o a mano escribiendo en la consola.
  - El output es el mismo que el esperado.
- hairyscary.cil
  - No funciona
    - Can't expand stack segment by 8 bytes to 524288 bytes
    - Use -lstack # with # > 524288
  - Problema en el init de los atributos, con los case al parecer. Ciclo de llamados infinitos