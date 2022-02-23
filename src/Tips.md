# Tips

- Para correr una carpeta de test especifica:
  - pytest -m \<NombreDeLaCarpeta\>
  - Ejemplo: pytest -m lexer

- En el launch.json hay dos configuraciones para debuguear
  - En una se genera codigo mips de testing.cl
  - En otra se interpreta el AST de CIL que sale del programa testing.cl
  - Entonces puedes comentar una u otra en dependencia de lo que te haga falta
  - Puedes cambiar facilmente el codigo que estas probando copiandolo a testing.cl tambien.

- Para correr un codigo mips:
  - spim -file \<Archivo\>

- Para pasarle input al spim y para guardar la salida:
  - spim -file \<Archivo\> \< input.txt
  - spim -file \<Archivo\> \< input.txt \> output.txt
