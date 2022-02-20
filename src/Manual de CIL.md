# MANUAL DE CIL

## RESTRICCIONES

## INSTRUCCIONES

### Tipos

Se inicializa la sección de tipos con :

```python
.TYPES
```

y se agrega una nueva definición de tipo según sea necesario de la siguiente manera :

``` python
.TYPES

type <name> {
    # PARENT (ONLY ONE)
    parent: <None or other type>

    # ATTRIBUTES
    attribute <attribute>
    ...
    ...
    ...
    
    # METHODS
    method <method_name>: <function>
    ...
    ...
    ...
}
```

Aqui vemos el ejemplo del tipo Main:

``` python
.TYPES

type Main {
    parent: IO

    attribute a
    attribute b

    method __init: __init_Main_type
    method __init_a_at_Main: __init_a_at_Main
    method __init_b_at_Main: __init_b_at_Main
    method abort: function_abort_at_Object
    method type_name: function_type_name_at_Object
    method copy: function_copy_at_Object
    method out_string: function_out_string_at_IO
    method out_int: function_out_int_at_IO
    method in_string: function_in_string_at_IO
    method in_int: function_in_int_at_IO
    method main: function_main_at_Main
}
```

### Datos

Se inicializa la sección de datos con :

``` python
.DATA
```

y se agrega una nueva definición de dato según sea necesario de la siguiente manera :

``` python
.DATA

   # CADENAS CONSTANTES
   <constant_name> = <value>
    ...
    ...
    ...
```

Aqui vemos el ejemplo de la cadena constante "Hola Mundo":

``` python
.DATA

string_hola_mundo = "Hola Mundo"
```

### Código

Se inicializa la sección de código con :

``` python
.CODE
```

y se agrega una nueva definición de código según sea necesario de la siguiente manera :

``` python
.CODE

    # FUNCIONES
    function <function_name> {
        # PARAMETERS
        PARAM <parameter_name>
        ...
        ...
        ...

        # LOCAL VARIABLES
        LOCAL <local_variable_name>
        ...
        ...
        ...

        # CODE
        <instruction>
        ...
        ...
        ...

        # RETURN
        RETURN <value>
    }
```

Aqui vemos el ejemplo de la funcion main:

``` python

.CODE
function function_main_at_Main {
 PARAM self

 LOCAL local_main_at_Main_internal_0
 LOCAL local_main_at_Main_internal_1

 local_main_at_Main_internal_0 = LOAD data_0
 ARG self
 ARG local_main_at_Main_internal_0
 local_main_at_Main_internal_1 = CALL function_out_string_at_IO
 
 RETURN local_main_at_Main_internal_1
}
```

### KeyWords

* PARAM
    > Indica que la función acepta el parametro siguiente al comando

    ```python
    # Ejemplo
    PARAM self
    ```

* LOCAL
    > Indica que la función acepta la variable local siguiente al comando

    ```python
    # Ejemplo
    LOCAL local_main_at_Main_internal_0
    ```

* RETURN
    > Indica que la función retorna la siguiente expresion

    ```python
    # Ejemplo
    RETURN local_main_at_Main_internal_1
    ```

* ARG
    > Indica que el proximo llamado a **CALL** acepta el argumento siguiente al comando

    ```python
    # Ejemplo
    ARG self
    CALL __init_Main_type
    ```

* CALL
    >Indica que la siguiente expresion es una llamada a una función

    ```python
    # Ejemplo
    ARG self
    CALL __init_Main_type
    ```

* LOAD
    >Indica que la siguiente expresion es una carga de un dato

    ```python
    # Ejemplo
    LOAD data_0
    ```

* LABEL
    >Indica que la siguiente expresion es una etiqueta

    ```python
    # Ejemplo
    LABEL label_0
    ```

    >Etiquetas son utilizadas para definir un punto de entrada a una parte del código tanto para ciclos como para anotaciones.

* VOID
    >Hace funcion de null

    ```python
    # Ejemplo
    local_distance_internal_3 = VOID
    ```

    >Para indicar que una variable no tiene un valor.

* IFGOTO
    >Indica que la siguiente expresion es una condicion y que se debe ir a la etiqueta siguiente al comando GOTO de cumplirse la condicion

    ```python
    # Ejemplo
    IF local_distance_internal_3 == VOID GOTO label_1
    ```

* GOTO
    >Indica que se debe ir a la etiqueta siguiente al comando

    ```python
    # Ejemplo
    GOTO label_1
    ```

* EQUAL
    >Indica si dos expresiones son iguales

    ```python
    # Ejemplo
    EQUAL local_distance_internal_3 VOID
    ```

* FATHER
    >Devuelve el padre del tipo del siguente objeto

    ```python
    # Ejemplo
    father = FATHER local_distance_internal_3
    ```

* ABORT
    >Indica que se debe abortar la ejecucion del programa

    ```python
    # Ejemplo
    ABORT
    ```

* TYPEOF
    >Devuelve el tipo del siguente objeto

    ```python
    # Ejemplo
    a = TYPEOF local_distance_internal_3
    ```

* COPY
    >Copia el valor de un objeto a otro objeto

    ```python
    # Ejemplo
    a = COPY local_distance_internal_3
    ```

* LENGTH
    >Devuelve la longitud de un objeto

    ```python
    # Ejemplo
    a = LENGTH local_distance_internal_3
    ```

* CONCAT
    > Devuelve la concatenacion de dos objetos

    ```python
    # Ejemplo
    a = CONCAT b c
    ```

* SUBSTRING
    > Devuelve una subcadena de un objeto

    ```python
    # Ejemplo
    a = SUBSTRING b c lenght
    ```

* PRINT
    > Imprime un objeto

    ```python
    # Ejemplo
    PRINT a
    ````

