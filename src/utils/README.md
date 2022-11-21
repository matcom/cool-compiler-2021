## Universidad de la Habana 2020
## Segundo proyecto de Compilacion

### Integrantes:
#### Yasmin Cisneros Cimadevila
#### Jessy Gigato Izquierdo
#### C-311

Para la ejecución del programa nos apoyamos en la api-cli brindada por el paquete de python typer la cual resulta bastante sencilla, con solo ejecutar:

    python3 pipeline.py --help

se mostrará un menú de instrucciones:

    Usage: pipeline.py [OPTIONS] COMMAND [ARGS]...

    Options:
    --install-completion  Install completion for the current shell.
    --show-completion     Show completion for the current shell, to copy it or
                            customize the installation.

    --help                Show this message and exit.

    Commands:
    test-context
    test-execution
    test-inference
    test-parse
    test-semantics
    tokenize

Los comandos principales serían:

    test-execution
    test-semantics

- `text'semantics` recibe un archivo .cl con un programa en COOL con tipos `AUTO_TYPE`  y devuelve un programa en COOL con todos los `AUTO_TYPE` reemplazados por sus tipos correspondientes.

- `test-execution` el cual recibe como entrada un archivo .cl con un programa en COOL y ejecuta dicho programa.

Los casos pruebas se encuentran en las siguientes direcciones:

    testing/semantic
    testing/inference

un ejemplo de la ejecución sería:

    python3 pipeline.py test-execution testing/inference/program12.cl 

